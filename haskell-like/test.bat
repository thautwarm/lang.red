python ./testLang.py expression "a => a+1"  -o lambda
python ./testLang.py expression "b:int->int->int => a+1"  -o left_recur_typedef
python ./testLang.py expression " 1+2 |> 2*3 or 5"  -o dual_operation
python ./testLang.py expression "not 1? + not 2??"  -o bool_and_null_query
python ./testLang.py expression "f = x:int->int =>{ when x(2)==2 then true otherwise then true  } " -o guard -testTk True
python ./testLang.py expression "f(1.0)(x)(y) = { x(y) + 20 } " -o pattern_matching