describe "Basic Test Suite", ->
  it "Basic boolean test", ->
    expect(true).toBe true
    expect(false).not.toBe true

  it "Basic math test", ->
    add = (a, b) ->
      a + b
    expect(add(2, 2)).toEqual 4

  it "Basic array test", ->
    arr = [1, true, 'apple']
    expect(arr).toContain('apple')
