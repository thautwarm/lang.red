## 学习语言设计中

[像做得像Hasekell结果一点也不想Haskell的语言](https://github.com/thautwarm/lang.red/tree/master/haskell-like)
```
c = "license"
f(head::tail)([a, b, ~c])
        when a==b then head
g(a:int, 1)(b:int, 2)(c:int, 3):int = 
        when a == b then c
        when b == c then a
        when a == c then b
        otherwise   then summary
    where summary = a+b+c
```

- [文法](https://github.com/thautwarm/lang.red/blob/master/haskell-like/grammar)

- [测试Script](https://github.com/thautwarm/lang.red/blob/master/haskell-like/test.hs)以及[测试结果文件集](https://github.com/thautwarm/lang.red/tree/master/haskell-like/tested)


