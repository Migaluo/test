def findMinAndMax(list):
    if list(len)==0:
        return (None,None)
    else:
        min=max=list[0]
        for number in list:
            if number>max:
                max=number
            elif number<min:
                min=number
        return(max,min)

