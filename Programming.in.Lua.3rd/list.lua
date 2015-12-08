local List = {}
function List.new()
    return {first = 0, last = -1}
end

function List.pushfirst(lst, value)
    local first = lst.first - 1
    lst[first] = value
    lst.first = first
end

function List.pushlast(lst, value)
    local last = lst.last + 1
    lst[last] = value
    lst.last = last
end

function List.popfirst(lst)
    local first = lst.first
    if (first > lst.last) then error("list is empty") end
    local value = lst[first]
    list[first] = nil
    list.first = first + 1
    return value
end

function List.poplast(lst)
    local last = lst.last
    if (lst.first > last) then error("list is empty") end
    lst[last] = nil
    lst.last = last - 1
    return value
end
return List

