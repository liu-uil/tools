#encoding = utf-8

def insert_sort(lists):
    count = len(lists)
    for i in range(1, count):
        key = lists[i]
        j = i-1
        while j >= 0:
            if lists[j]>key:
                lists[j+1] = lists[j]
                lists[j] = key
            j-=1
    
    return lists

def bubble_sort(lists):
    count = len(lists)
    for i in range(0, count):
        for j in range(0, count-i-1):
            if lists[j] > lists[j+1]:
                lists[j], lists[j+1] = lists[j+1], lists[j]

    return lists

def quick_sort(lists, left, right):
    if left >= right:
        return lists
    left2 = left
    right2 = right
    key = lists[left]
    while left < right:
        while right > left and lists[right] >= key:
            right-=1
        lists[left] = lists[right]
        while left < right and lists[left] <= key:
            left+=1
        lists[right] = lists[left]
    lists[right] = key
    quick_sort(lists, left2, left-1)
    quick_sort(lists, left+1, right2)
    return lists

if __name__=='__main__':
    testLists = [4,5,7,2,1,7,10,30,27,-10,-3,36]
    print testLists
    left = 0
    right = len(testLists)-1
    quick_sort(testLists, left, right)
    print testLists
    