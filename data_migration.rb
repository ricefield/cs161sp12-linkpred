require 'rubygems'
require 'ruby-debug'
require 'redis'

# Data in the form:
# 100000003530958471380   0   1   116685854800710466759   Jul:2011:17:12:47+0000

class RedisAdapter

  def initialize(file_name)
    @input = file_name
    @snapshot = file_name.split(".").first
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
    File.open(@input).each do |entry|
      puts "Reading from #{@input}"
      uid, type, num = entry.split # strings
      links = entry.split[3,num.to_i] # users "related" to specified user uid
      #timestamp = entry[entry.lenth-1] # not using this for now...very fine granularity

      if type == '0'
        links.each { |i| add_interest_to_set(uid, i) }
      else type == '1'
        links.each { |i| add_fan_to_set(uid, i) }
      end
      add_user(uid)
    end
    puts "Finished reading input."
    puts "Finished migration from #{@input} to redis server."
  end

  # == Definition ==
  # Adds the specified interest_uid to the set of users that 
  # the specified user has added to his circles.
  # @param uid a given user
  # @param interest_uid the uid of a person added by the given user
  def add_interest_to_set(uid, interest_uid)
    @redis.sadd "#{@snapshot}:#{uid}:interests", interest_uid
  end

  # == Definition ==
  # Adds the specified fan_uid to the set of users that 
  # have added the specified user to their circles.
  # @param uid a given user
  # @param fan_uid the uid of a person that has added the given user
  def add_fan_to_set(uid, fan_uid)
    @redis.sadd "#{@snapshot}:#{uid}:fans", fan_uid
  end

  # == Definition ==
  # Adds the specified uid to a cumulative set of all uid's in the
  # given snapshot
  def add_user(uid)
    @redis.sadd "#{@snapshot}:users", uid
  end

  # == Definition ==
  # Returns the number of users in the snapshot
  def num_users
    @redis.scard "#{@snapshot}:users" if @redis
  end

  # == Definition ==
  # Returns an array of the users in the snapshot
  def get_users
    @redis.smembers "#{@snapshot}:users" if @redis
  end

  # == Definition ==
  # Returns the number of interests of a given user
  def num_interests(uid)
    @redis.scard "#{@snapshot}:#{uid}:interests" if @redis
  end

  # == Definition ==
  # Returns an array of the interests of a given user
  def get_interests(uid)
    @redis.smembers "#{@snapshot}:#{uid}:interests" if @redis
  end

  # == Definition ==
  # Returns the number of fans of a given user
  def num_fans(uid)
    @redis.scard "#{@snapshot}:#{uid}:fans" if @redis
  end

  # == Definition ==
  # Returns an array of the fans of a given user
  def get_fans(uid)
    @redis.smembers "#{@snapshot}:#{uid}:interests" if @redis
  end

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
end


migrator = RedisAdapter.new("test-graph-2011-07-04.txt")
migrator.connect
migrator.migrate

puts "\n================================="
puts "============ SUMMARY ============"
puts "================================="
puts "\nSize of users set: #{migrator.num_users}"
puts "Members in users set:"
users = migrator.get_users
puts users.inspect

puts "\n================================="
puts "============ DETAILS ============"
puts "=================================\n"
puts ""
users.each do |uid|
  puts "User #{uid}:"
  puts "Size of interests set:  #{migrator.num_interests(uid)}"
  puts "Members in interests set: #{migrator.get_interests(uid).inspect}"
  puts "Size of fans set:  #{migrator.num_fans(uid)}"
  puts "Members in fans set: #{migrator.get_fans(uid).inspect}"
  puts "\n==============================="
  puts ""
end


# Skeleton code for what Brian could use
#puts migrator.shared_interests(users[0], users[1]).inspect
#puts migrator.combined_interests(users[0], users[1]).inspect
#puts migrator.mutual_friends(users[0]).inspect
