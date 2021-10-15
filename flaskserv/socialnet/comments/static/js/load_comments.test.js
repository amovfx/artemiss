
const lib = require('../../../assets/js/infinite_scroller')

test('should output name and age', () => {
    var val = lib.addNum(2,3)
    expect(val).toBe(5)
});

test('should output name and age', () => {
    var val = lib.sub(3,2)
    expect(val).toBe(1)
});
