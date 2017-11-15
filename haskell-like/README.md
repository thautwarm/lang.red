并不是很像HS.

## Requirement 
- [EBNFParser >= 1.0.1](https://github.com/thautwarm/EBNFParser)  
This is a parser generator framework written by myself, you can think it as `antlr` for Python community.

## 关于进展 

- [Grammar v0.1](./grammar)

- [Test Shell Script](./test.sh)

- [Tested Directory](./tested)

## Take a shot
```
f(x)(head|tail)(y) = 

    when head > x(y) then {
        x + y 
        }
    
    when head == y then head |> x 
    
    otherwise then null
```
## 为什么要写这个? 
因为用Python模仿Haskell很舒服。

## 为什么不全部模仿
因为啊， haskell的parser应该有上下文有关的部分, EBNFParser解决不来的，当然也可能是我智商不够  
(刚刚突然想到怎么实现游标卡尺XD  
而且我想要把parser的顶部做成一个expression。  



## 语法
一切皆表达式，即便只是从parser上来说。  
- 定义 `=`
```
a = 1

f(x)([head::tail]) = head + x*f(x-1)(tail) 

f(x: int, [head::tail]: my_list) = head + step + (tail) # : 是 类型声明
    where step = x*f(x-1) # call by name. 
    #  默认提取符号的作用域在等式左端参数导入之后， 等式右端表达式解析之前。
       如果没有找到需要的符号， 放置一个hook，等待该作用域里定义了对应符号后链接过去。

f(1+2)(~g(~x)) = 5   #  `~` 表示寻找最近作用域某变量的引用。此处定义了一个模式匹配的函数。 

f(2:int) = 5

f(2:double) = -5  # 类型的模式匹配

```

- 常量
```Python
False, True, None
```

- Guard
```
a(x)= 
    when x%8==1 then x
    when x$8==2 then 2*x
    otherwise   then -x
```

- Parameters that Passed By Name
```
if(test)(`if_true)(`else) =  # 传参时不求值
    {
    `if_true |> println    # pipeline
    when test then if_true
    otherwise then else
    }
    
```

- Lambda
```
() => 1
(1:int) => 2
(head::tail, [a, b, c]) => 
        when a == b == c then head * a
        when a + b == c  then head - c
        otherwise then tail[0]  #  支持数组slice
```

- List Comprehension
```
[a+1 where [a,b] from [[1,2], [2,3], [3,4]], a + b >= 5]

#  类比语法
#  [a+1 | a<-[(1,2), (2,3), (3,4)], a + b >= 5]
#  [a+1 for a in [(1,2),(2,3),(3,4)] if a + b >= 5]
```

