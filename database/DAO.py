from database.DB_connect import DBConnect
from model.circuito import Circuit
from model.risultato import Risultato


class DAO():
    @staticmethod
    def getAllCircuits():
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """SELECT * 
                    from circuits"""
        cursor.execute(query)

        res = []
        for row in cursor:
            res.append(Circuit(row['circuitId'], row['circuitRef'], row['name'], row['location'], row['country'],
                               row['lat'], row['lng'], row['alt'], row['url'], {}))

        cursor.close()
        cnx.close()
        return res

    @staticmethod
    def get_years():
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """SELECT DISTINCT s.`year` as anno
                    FROM seasons s"""
        cursor.execute(query)

        res = []
        for row in cursor:
            res.append(row['anno'])

        cursor.close()
        cnx.close()
        return res

    @staticmethod
    def get_valori(circuito, anno):
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """SELECT re.driverId as d, re.`time` as t
                    FROM results re, races r
                    WHERE r.raceId = re.raceId
                        and r.circuitId = %s
                        and r.`year` = %s"""
        cursor.execute(query, (circuito.circuitId, anno))

        res = []
        for row in cursor:
            res.append(Risultato(**row))

        cursor.close()
        cnx.close()
        return res

    @staticmethod
    def getAllArchi(anno1, anno2):
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """SELECT t1.c1 as c1, t2.c2 as c2, p1+p2 as peso
                    FROM (SELECT r.circuitId as c1, COUNT(*) as p1
                            FROM races r, results re 
                            WHERE r.raceId = re.raceId
                                and %s < r.`year` 
                                and r.`year`< %s
                                and re.`time`  is not null
                            GROUP BY r.circuitId) t1, 
                            (SELECT r.circuitId as c2, COUNT(*) as p2
                                FROM races r, results re 
                                WHERE r.raceId = re.raceId
                                    and %s < r.`year` 
                                    and r.`year`< %s
                                    and re.`time`  is not null
                                GROUP BY r.circuitId) t2
                    WHERE t1.c1 < t2.c2"""
        cursor.execute(query, (anno1, anno2, anno1, anno2))

        res = []
        for row in cursor:
            res.append((row['c1'], row['c2'], row['peso']))

        cursor.close()
        cnx.close()
        return res
