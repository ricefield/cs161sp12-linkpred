require 'redis'

# Data in the form:
# 100000003530958471380   0   1   116685854800710466759   Jul:2011:17:12:47+0000

class RedisAdapter
  attr_accessor :snapshot, :snapshot2

  def initialize(file_name1, file_name2 = nil)
    @input = file_name1
    @snapshot = file_name1.split(".").first if file_name1

    # TODO: determine if this is necessary
    # NOTE: following 2 variables are currently unused
    # I added them for later when we want to analyze our predictions
    # across snapshots
    @input2 = file_name2
    @snapshot2 = file_name2.split(".").first if file_name2
  end

  def connect
    begin
      puts "Connecting to Redis..."
      @redis = Redis.new
      @redis.ping
    rescue Errno::ECONNREFUSED => e
      puts "Error: Redis server unavailable. Shutting down..."
      exit 1
    end
  end


  # Note: adds data to the following 3 sets
  # 1) #{snapshot}:#{uid}:interests
  # 2) #{snapshot}:#{uid}:fans
  # 3) #{snapshot}:users
  def migrate
    puts "Preparing to migrate..."

    # Migrate the initial snapshot
    puts "Reading from #{@input}"
    File.open(@input).each do |entry|
      #puts "Reading from #{@input}"
      uid, type, num = entry.split # strings
      links = entry.split[3,num.to_i] # users "related" to specified user uid
      #timestamp = entry[entry.lenth-1] # not using this for now...very fine granularity

      if type == '0'
        links.each { |i| add_interest_to_set(uid, i, @snapshot) }
      else type == '1'
        links.each { |i| add_fan_to_set(uid, i, @snapshot) }
      end
      add_user(uid, @snapshot)
    end

    # Migrate the second snapshot for comparison, if it exists
    if @input2
      puts "Reading from #{@input2}"
      File.open(@input2).each do |entry|
        #puts "Reading from #{@input2}"
        uid, type, num = entry.split # strings
        links = entry.split[3,num.to_i] # users "related" to specified user uid
        #timestamp = entry[entry.lenth-1] # not using this for now...very fine granularity
        
        if type == '0'
          links.each { |i| add_interest_to_set(uid, i, @snapshot2) }
        else type == '1'
          links.each { |i| add_fan_to_set(uid, i, @snapshot2) }
        end
        add_user(uid, @snapshot2)
      end
    end
    
    puts "Finished reading input."
    puts "Finished migration from #{@input} to redis server."
  end

  # == Definition ==
  # Adds the specified interest_uid to the set of users that 
  # the specified user has added to his circles.
  # @param uid a given user
  # @param interest_uid the uid of a person added by the given user
  def add_interest_to_set(uid, interest_uid, snapshot)
    @redis.sadd "#{snapshot}:#{uid}:interests", interest_uid
  end

  # == Definition ==
  # Adds the specified fan_uid to the set of users that 
  # have added the specified user to their circles.
  # @param uid a given user
  # @param fan_uid the uid of a person that has added the given user
  def add_fan_to_set(uid, fan_uid, snapshot)
    @redis.sadd "#{snapshot}:#{uid}:fans", fan_uid
  end

  # == Definition ==
  # Adds the specified uid to a cumulative set of all uid's in the
  # given snapshot
  def add_user(uid, snapshot)
    @redis.sadd "#{snapshot}:users", uid
  end

  # == Definition ==
  # Returns the number of users in the snapshot
  def num_users(snapshot)
    @redis.scard "#{snapshot}:users" if @redis
  end

  # == Definition ==
  # Returns an array of the users in the snapshot
  def get_users(snapshot)
    @redis.smembers "#{snapshot}:users" if @redis
  end

  # == Definition ==
  # Returns the number of interests of a given user
  def num_interests(uid, snapshot)
    @redis.scard "#{snapshot}:#{uid}:interests" if @redis
  end

  # == Definition ==
  # Returns an array of the interests of a given user
  def get_interests(uid, snapshot)
    @redis.smembers "#{snapshot}:#{uid}:interests" if @redis
  end

  # == Definition ==
  # Returns the number of fans of a given user
  def num_fans(uid, snapshot)
    @redis.scard "#{snapshot}:#{uid}:fans" if @redis
  end

  # == Definition ==
  # Returns an array of the fans of a given user
  def get_fans(uid, snapshot)
    @redis.smembers "#{snapshot}:#{uid}:fans" if @redis
  end

  def new_interests(uid, snapshot, snapshot2)
    @redis.sdiff "#{snapshot2}:#{uid}:interests", "#{snapshot}:#{uid}:interests"
  end

  def new_fans(uid, snapshot, snapshot2)
    @redis.sdiff "#{snapshot2}:#{uid}:fans", "#{snapshot}:#{uid}:fans"
  end

  def existing_interests(uid, snapshot, snapshot2)
    @redis.sinter "#{snapshot2}:#{uid}:interests", "#{snapshot}:#{uid}:interests"
  end

  def existing_fans(uid, snapshot, snapshot2)
    @redis.sinter "#{snapshot2}:#{uid}:fans", "#{snapshot}:#{uid}:fans"
  end

  # Edge in form "a,b" for a->b edge formed, aka 
  # a became a fan of b, meaning a was in b's 1 row
  # and b is in a's 0 row
  def add_new_edge(snapshot, snapshot2, edge)
    @redis.sadd "#{snapshot}:#{snapshot2}:followbacks", edge
  end

  def get_followbacks(snapshot, snapshot2)
    @redis.smembers "#{snapshot}:#{snapshot2}:followbacks" if @redis
  end

#### TODO
=begin
  # == Definition ==
  # Returns an array of the shared interests of uid1 and uid2
  def shared_interests(uid1, uid2)
    @redis.sinter "#{@snapshot}:#{uid1}:interests", "#{@snapshot}:#{uid2}:interests"
  end

  # == Definition ==
  # Returns an array of the combined interests of uid1 and uid2
  # Note: not sure if this is useful/needed
  def combined_interests(uid1, uid2)
    @redis.sunion "#{@snapshot}:#{uid1}:interests", "#{@snapshot}:#{uid2}:interests"
  end
  
  # == Definition ==
  # Returns an array of the mutual friends of uid
  def mutual_friends(uid)
    @redis.sinter "#{@snapshot}:#{uid}:interests", "#{@snapshot}:#{uid}:fans"
  end

  # == Definition ==
  # Returns an array of the shared mutual friends of uid1 and uid2
  def shared_mutual_friends(uid1, uid2)
    # Get the mutual friends for both users, and then intersection
    # of those sets represents the shared mutual friends
    mutual_friends(uid1) & mutual_friends(uid2)
  end
=end

end


migrator = RedisAdapter.new("graph-2011-07-04.txt") #,"graph-2011-08-04.txt")
migrator.connect
migrator.migrate


puts "\n==================================================="
puts "=========== SUMMARY OF INITIAL SNAPSHOT ==========="
puts "==================================================="
puts "\nSize of users set: #{migrator.num_users(migrator.snapshot)}"
#puts "Members in users set:"
users = migrator.get_users(migrator.snapshot) # Gets users from the INITIAL snapshot
#puts users.inspect


=begin
puts "\n==================================================="
puts "=========== DETAILS OF INITIAL SNAPSHOT ==========="
puts "===================================================\n"
puts ""
users.each do |uid|
  puts "User #{uid}:"
  puts "Size of interests set:  #{migrator.num_interests(uid, migrator.snapshot)}"
  puts "Members in interests set: #{migrator.get_interests(uid, migrator.snapshot).inspect}"
  puts "Size of fans set:  #{migrator.num_fans(uid, migrator.snapshot)}"
  puts "Members in fans set: #{migrator.get_fans(uid, migrator.snapshot).inspect}"
  puts "\n==============================="
  puts ""
end

puts "\n=================================================="
puts "=========== SUMMARY OF SECOND SNAPSHOT ==========="
puts "=================================================="
puts "\nSize of users set: #{migrator.num_users(migrator.snapshot2)}"
puts "Members in users set:"
users = migrator.get_users(migrator.snapshot2)
puts users.inspect

puts "\n=================================================="
puts "=========== DETAILS OF SECOND SNAPSHOT ==========="
puts "==================================================\n"
puts ""
users.each do |uid|
  puts "User #{uid}:"
  puts "Size of interests set:  #{migrator.num_interests(uid, migrator.snapshot2)}"
  puts "Members in interests set: #{migrator.get_interests(uid, migrator.snapshot2).inspect}"
  puts "Size of fans set:  #{migrator.num_fans(uid, migrator.snapshot2)}"
  puts "Members in fans set: #{migrator.get_fans(uid, migrator.snapshot2).inspect}"
  puts "\n==============================="
  puts ""
end



puts "\n=============================================="
puts "=============  SUMMARY OF DIFF ==============="
puts "==============================================\n"

users.each do |uid|
  new_interests = migrator.new_interests(uid, migrator.snapshot, migrator.snapshot2)
  existing_interests = migrator.existing_interests(uid, migrator.snapshot, migrator.snapshot2)
  new_fans = migrator.new_fans(uid, migrator.snapshot, migrator.snapshot2)
  existing_fans = migrator.existing_fans(uid, migrator.snapshot, migrator.snapshot2)
  puts "User #{uid}"
  puts "Size of New interests set: #{new_interests.size}"
  puts "New interests set: #{new_interests.inspect}"
  puts "Size of Existing interests set: #{existing_interests.size}"
  puts "Existing interests set: #{existing_interests.inspect}"

  puts "Size of New fans set: #{new_fans.size}"
  puts "New fans set: #{new_fans.inspect}"
  puts "Size of Existing fans set: #{existing_fans.size}"
  puts "Existing fans set: #{existing_fans.inspect}"
  puts "\n==============================="
  puts ""
end
=end



# THE FOLLOWING CODE INSERTS THE FOLLOWBACKS INTO THE REDIS-DB
# It's like for every user, if it has another user in BOTH sets,
# then check if it had the user in only ONE set previously, then that is
# a mutual friend acceptance. "a, b" means edge a->b formed

puts "PARSING FOR FOLLOWBACKS..."
users.each do |uid|
  new_interests = migrator.new_interests(uid, migrator.snapshot, migrator.snapshot2)
  existing_interests = migrator.existing_interests(uid, migrator.snapshot, migrator.snapshot2)
  new_fans = migrator.new_fans(uid, migrator.snapshot, migrator.snapshot2)
  existing_fans = migrator.existing_fans(uid, migrator.snapshot, migrator.snapshot2)

  new_interests.each do |ni|
    if existing_fans.include?(ni) # so b->a already existed
      #puts "ADDING NEW INTEREST FOLLOWBACK #{uid}, #{ni}"
      migrator.add_new_edge(migrator.snapshot, migrator.snapshot2, "#{uid}, #{ni}")
    end
  end

  # NOTE: technically we don't need this because the data is reflective
  # so if you are a new fan here, that means you were a new interest elsewhere
  # HOWEVER: it is useful if we have missing data in the dataset, then this could
  # reveal new information, so it doesn't really hurt, unless it becomes really slow
  
  # NOTE: commented out this next loop to hopefully make it run faster...
=begin
  new_fans.each do |nf|
    if existing_interests.include?(nf)
      puts "ADDING NEW FAN FOLLOWBACK #{nf}, #{uid}"
      migrator.add_new_edge(migrator.snapshot, migrator.snapshot2, "#{nf}, #{uid}")
    end
  end
=end

end



puts "\n================================================="
puts "============= FOLLOWBACKS SUMMARY ==============="
puts "=================================================\n"
puts "Number of new followbacks:"
puts migrator.get_followbacks(migrator.snapshot, migrator.snapshot2).count
#puts "Array of followbacks in form 'a,b' for followback a->b"
#puts migrator.get_followbacks(migrator.snapshot, migrator.snapshot2).inspect

