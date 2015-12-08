module("set", package.seeall)

local mt = { __metatable = "Metatable for sets" }
local Set = {}

function Set.new(lst)
    local set = {}
    setmetatable(set, mt)
    for _, v in ipairs(lst) do
        set[v] = true
    end
    return set
end


function Set.union(a, b)
--    if getmetatable(a) ~= mt or getmetatable(b) ~= mt then
--        error("attempt to 'add' a set with a non-set value", 2)
--    end

    local res = Set.new{}
    for k in pairs(a) do res[k] = true end
    for k in pairs(b) do res[k] = true end
    return res
end
mt.__add = Set.union

function Set.intersection(a, b)
--    if getmetatable(a) ~= mt or getmetatable(b) ~= mt then
--        error("attempt to 'add' a set with a non-set value", 2)
--    end

    local res = Set.new{}
    for k in pairs(a) do
        res[k] = b[k]
    end
    return res
end
mt.__mul = Set.intersection

function Set.difference(a, b)
    local res = Set.new{}
    for k in pairs(a) do
        if not b[k] then
            res[k] = true
        end
    end
    return res
end
mt.__sub = Set.difference

mt.__le = function(a, b)
    for k in pairs(a) do
        if not b[k] then return false end
    end
    return true
end

mt.__lt = function(a, b)
    return a <= b and not (b <= a)
end

mt.__eq = function(a, b)
    return a <= b and b <= a
end

function Set.tostring(set)
    local lst = {}
    for e in pairs(set) do
        lst[#lst + 1] = e
    end
    return "{" .. table.concat(lst, ", ") .. "}"
end
mt.__tostring = Set.tostring

function Set.print(set)
    print(Set.tostring(set))
end

return Set
