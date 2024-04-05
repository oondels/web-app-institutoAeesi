from datetime import date, datetime

mes_pagamento = "03-04-2024"

format = "%d-%m-%Y"
if datetime.strptime(mes_pagamento, format):
    print(mes_pagamento)
else:
    print("error")