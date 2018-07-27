def unitConversion(value, unit_in, unit_out):
    units = {'gal':1, 'qt':4, 'pt':8, 'cups':16, 'oz':128, 'tbsp':256, 'tsp': 768, 'mL':3800, 'L':3.8}
    return value * units[unit_out]/units[unit_in]

def bestValue(value):
    units = ["gal","L","cups","oz","tbsp","tsp","mL"]

    for unit in units:
        convert = unitConversion(value,"mL",unit)
        if unit is "cups" and convert >= 0.25:
            return (convert,unit)
        if convert > 1:
            return (convert,unit)
    return (value, "mL")