describe("Test timeslots.js", function() {
  it("test variable test to be 1", function(){
      var x = TestVariable;
      expect(x).toBeDefined();
      expect(x).toEqual(11);
  });

  it("test orginalTimeSlotsToBeUndefined", function(){
    expect(originalTimeslots).toBeUndefined();
  })

  it("test dayHalfHoursGeneratorHelper", function(){
    var times = dayHalfHoursGeneratorHelper();
    expect(times[0]).toEqual("00:00:00");
    expect(times[23]).toEqual("11:30:00");
    expect(times[47]).toEqual("23:30:00");
  })

  it("test timeFormat", function(){
    expect(timeFormat("00")).toEqual(" 0AM");
    expect(timeFormat("09")).toEqual(" 9AM");
    expect(timeFormat("10")).toEqual("10AM");
    expect(timeFormat("20")).toEqual(" 8PM");
    expect(timeFormat("22")).toEqual("10PM");
  })
});
