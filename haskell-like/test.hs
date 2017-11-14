-- 假HS


Obj :: Mutable a => () -> a
Obj = 1 -- lazy def

-- oo-style
Obj :  () -> [Mutable]  = 1

-- import
import sklearn.ensemble (
            RandomForestClassifier as rfc,
            RandomForestRegressor  as rfr)







