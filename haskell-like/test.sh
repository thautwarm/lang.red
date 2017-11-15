python ./testLang.py expression "(a) => a+1"  -o tested/lambda
python ./testLang.py expression "(b:int->int->int) => a+1"  -o tested/left_recur_typedef
python ./testLang.py expression " 1+2 |> 2*3 or 5"  -o tested/dual_operation
python ./testLang.py expression "not 1? + not 2??"  -o tested/bool_and_null_query
python ./testLang.py expression """f = (x:int->int) =>{
                                            when x(2)==2 then true
                                            when otherwise then true
                                            }""" -o tested/guard 
python ./testLang.py expression """f(1.0)(x)(y)={
                                            x(y) + 20
                                            }""" -o tested/pattern_matching



python ./testLang.py expression """f(x)(~head|tail)(y) = 
                                        when head > x(y) then {
                                            x + y 
                                            }
                                        
                                        when head == y then head |> x 
                                        
                                        otherwise then null""" -o tested/demo

python ./testLang.py expression '''if (test)(`and_then)(`else) = 
                                        when test then and_then
                                        otherwise then else''' -o tested/if_expr

python ./testLang.py expression '''result = if (1+2 == 5) (a2)("fafafa")
                                        where a2 = 10''' -o tested/demo
                                        # where 子句用于定义之后。