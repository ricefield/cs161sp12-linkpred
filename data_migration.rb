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
      add_user_to_set(uid)
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
    puts "AKJSDFAKLDJF INTEREST #{interest_uid}"
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
  def add_user_to_set(uid)
    @redis.sadd "#{@snapshot}:users", uid
  end

  # == Definition ==
  # Returns an array of the members in the specified set
  def set_members(set)
    @redis.smembers set if @redis
  end

  # == Definition ==
  # Returns the size of the specified set
  def set_size(set)
    @redis.scard set if @redis
  end
end


migrator = RedisAdapter.new("test-graph-2011-07-04.txt")
migrator.connect
migrator.migrate

puts "\n================================="
puts "============ SUMMARY ============"
puts "================================="
puts "\nSize of users set: #{migrator.set_size("test-graph-2011-07-04:users")}"
puts "Members in users set:"
users = migrator.set_members("test-graph-2011-07-04:users")
puts users.inspect

puts "\n================================="
puts "============ DETAILS ============"
puts "=================================\n"
puts ""
users.each do |uid|
  puts "User #{uid}:"
  puts "Size of interests set:  #{migrator.set_size("test-graph-2011-07-04:#{uid}:interests")}"
  puts "Members in interests set: #{migrator.set_members("test-graph-2011-07-04:#{uid}:interests").inspect}"
  puts "Size of fans set:  #{migrator.set_size("test-graph-2011-07-04:#{uid}:fans")}"
  puts "Members in fans set: #{migrator.set_members("test-graph-2011-07-04:#{uid}:fans").inspect}"
  puts "\n==============================="
  puts ""
end
