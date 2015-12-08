module("debugger", package.seeall)

function traceback()
    for level = 1, math.huge do
        local info = debug.getinfo(level, "Snl")
        if not info then break end
        if info.what == "C" then
            print(level, "C function ", info.name)
        else
            print(level, string.format("[%s:%d]", info.short_src, info.currentline), info.name)
        end
    end
end

function getvarvalue(name, level)
    local value
    local found = true
    level = (level or 1) + 1

    -- try local variables
    for i = 1, math.huge do
        local n, v = debug.getlocal(level, i)
        if not n then break end
        if n == name then
            value = v
            found = true
        end
    end
    if found then return value end

    -- try non-local variables
    local func = debug.getinfo(level, "f").func
    for i = 1, math.huge do
        local n, v = debug.getupvalue(func, i)
        if not n then break end
        if n == name then return v end
    end

    -- not found; get value from the environment
    local env = getvarvalue("_ENV", level)
    return env[name]
end

