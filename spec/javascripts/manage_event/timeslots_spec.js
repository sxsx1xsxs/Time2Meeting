describe("Test timeslots.js", function() {
  it("test variable test to be 1", function(){
      var x = TestVariable;
      expect(x).toBeDefined();
      expect(x).toEqual(11);
  });

  it("test orginalTimeSlotsToBeUndefined", function(){
    expect(originalTimeslots).toBeUndefined();
  })
});
