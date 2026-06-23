from database.DB_connect import DBConnect
from model.arco import Arco
from model.driver import Driver

class DAO():

    @staticmethod
    def getAllYears():
        conn = DBConnect.get_connection()
        results = []

        cursor = conn.cursor(dictionary=True)
        query = "SELECT distinct year FROM seasons s  ORDER BY year"

        cursor.execute(query)

        for row in cursor:
            results.append(row["year"])

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllNodes(year1, year2):
        conn = DBConnect.get_connection()
        results = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT DISTINCT d.*
                FROM drivers d, races r, results re
                WHERE r.raceId = re.raceId AND re.driverId = d.driverId  
                AND r.year BETWEEN %s AND %s
                AND re.position IS NOT NULL
                """

        cursor.execute(query, (year1, year2))

        for row in cursor:
            results.append(Driver(**row))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllEdges(year1, year2, idMapD):
        conn = DBConnect.get_connection()
        results = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT t1.driverId as id1, t2.driverId as id2, COUNT(*) as peso
                FROM (SELECT r.driverId, r.constructorId, r.raceId
                    FROM results r, races ra
                    WHERE r.raceId = ra.raceId
                    AND r.position IS NOT NULL
                    AND ra.year BETWEEN %s AND %s) as t1,
                (SELECT r.driverId, r.constructorId, r.raceId
                    FROM results r, races ra
                    WHERE r.raceId = ra.raceId
                    AND r.position IS NOT NULL
                    AND ra.year BETWEEN %s AND %s) as t2
                WHERE t1.constructorId = t2.constructorId
                AND t1.raceId = t2.raceId             
                AND t1.driverId > t2.driverId         
                GROUP BY t1.driverId, t2.driverId """

        cursor.execute(query, (year1, year2, year1, year2))

        for row in cursor:
            results.append(Arco(idMapD[row["id1"]], idMapD[row["id2"]], row["peso"]))

        cursor.close()
        conn.close()
        return results

