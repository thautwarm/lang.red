## Language I : Fairy
> How do you feel about a language totally made by expressions?   
> Moreover, pattern matching cound be found here and there :)   

[![build status](https://travis-ci.org/thautwarm/lang.red.svg?branch=master)](https://travis-ci.org/thautwarm/lang.red)
[![License](https://img.shields.io/badge/license-MIT-blue.svg?style=flat)](https://github.com/thautwarm/lang.red/blob/master/LICENSE)
[![help wanted](https://img.shields.io/badge/language-Fairy-green.svg?style=flat)](https://github.com/thautwarm/lang.red/pulls)
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

- [Grammar](https://github.com/thautwarm/lang.red/tree/master/fairy/grammar)

- [Test](https://github.com/thautwarm/lang.red/tree/master/fairy/test.hs)以及[测试结果文件集](https://github.com/thautwarm/lang.red/tree/master/fairy/tested)


