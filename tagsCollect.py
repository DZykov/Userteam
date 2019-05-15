#!/usr/bin/env python
# coding: utf-8


import pandas as pd
import json
import numpy as np


def makewieghts(params: dict) -> list:
    """
    Функция берёт словарь с двуями параметрами и возвращает лист с весами.
    """
    l = params["l"]
    coef = params["coef"]
    num = 1/2 - np.sqrt(5) / 2
    k = lambda x: 1/(x - num) + num

    def f(x):
        if k(x) > l:
            return l
        else:
            return k(x)
        
    wieghts = [0,0,0]
    wieghts[0] =f(coef)
    wieghts[1] = (f(coef) + f(1-coef)) / 2
    wieghts[2] = f(1 - coef)
    return wieghts


def readUserData(idUser: int) -> str:
    """
    Возвращает данные по пользователю
    """
    with open("data/" + str(idUser) + ".txt") as f:
        temp = "".join(f.readlines())
    return temp


def getUserCoef(idUser: int, params: dict) -> dict:
    """
    Возвращает параметры (coef и l) для пользователя
    """
    try:
        with open("usersSettings/" + str(idUser) + ".txt", "r") as f:
            params["coef"] = float(f.readlines()[0])
    except:
        with open("usersSettings/" + str(idUser) + ".txt", "w") as f:
            f.writelines(str(params["coef"]))
    return params


def readUserData(temp: str) -> dict:
    """
    Создает и вовзращает данные о пользователи ввиде таблицы/матрицы
    """
    try:
        keys = temp[1:-1].split(" ")[::2]
        values = temp[1:-1].split(" ")[1::2]
    except:
        keys = temp.keys()
        values = temp.values()
    keys = list(map(lambda x:x, keys))
    f = lambda x: list(map(int,list(filter(lambda x:x != "",x.split(",")))))

    def convertList(x):
        if len(x) > 1:
            return x
        else:
            return x[0]

    values = list(map(lambda x: f(x), values))
    userdata = dict(zip(keys, values))
    return userdata


def writeProcessDataUser(userdata: dict, params: dict, idUser: int) -> dataframe:
    """
    Возвразает все теги для пользователя с их баллами
    """
    tempuserdata = dict(userdata)

    try:
        del tempuserdata['posts-read']
    except:
        pass

    try:
        del tempuserdata['posts-visited']
    except:
        pass

    tagsuser = pd.DataFrame(tempuserdata).T
    
    tagsuser.columns = ["watch"]

    tagsuser["tags"] = tagsuser.index
    tagsuser["categ"] = tagsuser["tags"].map(lambda x: x.split("-")[0])
    tagsuser["tags"] = tagsuser["tags"].map(lambda x: x.split("-")[2])
    tagsuser.index = range(len(tagsuser))

    tagsuser.groupby(["tags"],as_index=False).mean()
    tagsuser["categ"] = tagsuser["categ"].map(dict(zip(["read","visit","view"],
                                   params["wieghts"])))
    tagsuser["temp"] = tagsuser["watch"] * tagsuser["categ"]
    r = tagsuser.groupby(["tags"])["temp"].sum()
    finalUserTags = r / tagsuser.groupby(["tags"])["watch"].sum()
    finalUserTags.sort_values(ascending=False)

    try:
        t = pd.DataFrame(finalUserTags)
    except:

        return t
    t.columns = ["score"]
    return t


def makeData(idUser: int, d: dataset, coef: float) -> dataframe:
    """
    Возвращает полный анализ и результат
    """
    params = {}
    params["l"] = 0.5
    params["coef"] = coef
    params["wieghts"] = makewieghts(params)
    temp = json.loads(d["tags"][idUser])
    if(temp == {}):
        raise ValueError
    userdata = readUserData(temp)
    t = writeProcessDataUser(userdata, params, str(idUser))
    return t


def makeLink(t, r):
    """
    Возвращает все статьи в убывающем интересе и интерес больше 0.
    """
    col = list(set(r.columns).intersection(set(t.index)))
    table = r[col].applymap(int)
    tableCoef = pd.DataFrame((np.array(table) * np.array(t.T[col])).T).T
    tableCoef.columns = col
    tableCoef["score"] = tableCoef.sum(axis=1)
    tableCoef["link"] = r["ids"]
    tableCoef = tableCoef.sort_values("score", ascending=False)
    return tableCoef[tableCoef["score"] > 0]
