# Dataset for breast cancer patients
recurrences = [
    {'Menopause=ge40': True, 'Menopause=lt40': False, 'Menopause=premeno': False, 'Inv-nodes=0-2': False, 'Inv-nodes=3-5': True, 'Inv-nodes=6-8': False, 'Deg-malig=3': True, 'Deg-malig=1': False, 'Deg-malig=2': False},
    {'Menopause=ge40': True, 'Menopause=lt40': False, 'Menopause=premeno': False, 'Inv-nodes=0-2': False, 'Inv-nodes=3-5': False, 'Inv-nodes=6-8': True, 'Deg-malig=3': True, 'Deg-malig=1': False, 'Deg-malig=2': False},
    {'Menopause=ge40': False, 'Menopause=lt40': False, 'Menopause=premeno': True, 'Inv-nodes=0-2': True, 'Inv-nodes=3-5': False, 'Inv-nodes=6-8': False, 'Deg-malig=3': True, 'Deg-malig=1': False, 'Deg-malig=2': False},
]


non_recurrences = [
    {'Menopause=ge40': False, 'Menopause=lt40': True, 'Menopause=premeno': False, 'Inv-nodes=0-2': True, 'Inv-nodes=3-5': False, 'Inv-nodes=6-8': False, 'Deg-malig=3': True, 'Deg-malig=1': False, 'Deg-malig=2': False},
    {'Menopause=ge40': True, 'Menopause=lt40': False, 'Menopause=premeno': False, 'Inv-nodes=0-2': True, 'Inv-nodes=3-5': False, 'Inv-nodes=6-8': False, 'Deg-malig=3': False, 'Deg-malig=1': False, 'Deg-malig=2': True},
    {'Menopause=ge40': False, 'Menopause=lt40': False, 'Menopause=premeno': True, 'Inv-nodes=0-2': True, 'Inv-nodes=3-5': False, 'Inv-nodes=6-8': False, 'Deg-malig=3': False, 'Deg-malig=1': True, 'Deg-malig=2': False},
]

initial_memory = {
    'Menopause=ge40': 5, 'Menopause=lt40': 5, 'Menopause=premeno': 5,
    'Inv-nodes=0-2': 5, 'Inv-nodes=3-5': 5, 'Inv-nodes=6-8': 5,
    'Deg-malig=1': 5, 'Deg-malig=2': 5, 'Deg-malig=3': 5,
    'NOT Menopause=ge40': 5, 'NOT Menopause=lt40': 5, 'NOT Menopause=premeno': 5,
    'NOT Inv-nodes=0-2': 5, 'NOT Inv-nodes=3-5': 5, 'NOT Inv-nodes=6-8': 5,
    'NOT Deg-malig=1': 5, 'NOT Deg-malig=2': 5, 'NOT Deg-malig=3': 5
}

R1 = {'Deg-malig=3', 'NOT Menopause=lt40'}  
R2 = {'Deg-malig=3'}  
R3 = {'Inv-nodes=0-2'} 