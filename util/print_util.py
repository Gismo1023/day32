
#print_util.py
#출력시 구분선과 함계 출력하는 함수
def pp(*obj):
    print(*obj)
    print('-'*80)

#type과 구분선 함께 출력하는 하뭇
def pt(*arg):
    print(type(*arg))
#개수만큼 구분석 출력하는 함수
