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
因为啊， haskell的parser应该有上下文有关的部分。  
而且我想要把parser的顶部做成一个expression。  



