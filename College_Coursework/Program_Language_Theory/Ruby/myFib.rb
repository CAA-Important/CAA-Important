def myFib(n)
    if(n < 0)
        return 0

    elsif(n == 0)
        return 1

    else
        return (myFib(n - 1) - (2 * myFib(n - 2)))
    end
end

number = myFib(ARGV[0].to_i)
puts("#{number}")   