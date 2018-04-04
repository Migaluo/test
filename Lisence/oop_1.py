class Solution(object):
    def foo(self, s):   # 2.此时s接收到ss
        def bar(a):     # 3.bar暂时没有调用不执行
            print(s)    #  5、 输出s 在2步已赋值ss
        bar("aa")       #  4、调用bar函数，传参是aa,但在此程序中没用到
Solution().foo("ss")     # 1.调用Solution中foo方法 传的参数是ss