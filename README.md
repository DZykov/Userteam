# Userteam
## Tprogger
![alt text](https://pp.userapi.com/c855024/v855024316/401f0/5KqVY1L3XV8.jpg)

### Использование:
tagsCollect - главный файл. Он делает всю работу.

```python
d = pd.read_csv("data/users_export_onesignal_users_2019-05-11T16_43_12+00_00.csv")
t = tagsCollect.makeData(userId, d, coef)
r = pd.read_csv("data/tagsConv.csv")
tempTable = tagsCollect.makeLink(t, r)
tempTable["score"] = "Интерес к статье " + tempTable["score"].map(lambda x:str(round(float(x))))
tempTable[["link","score"]]
numN = 6
temp = list(tempTable.head(numN)["link"]) # топ 6 статей по интересам
```
