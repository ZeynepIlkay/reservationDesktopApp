from ast import Index
import enum 
import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from panel import Ui_MainWindow
from database_connection import *
from datetime import datetime, timedelta
import requests
import json

# projenin ana dosyası (main.py)
import database_connection

#




#interface oparations
#-----------------------------


app = QApplication(sys.argv)
window = QMainWindow()
ui = Ui_MainWindow()  #panel
ui.setupUi(window)   #ui inside the panel
window.show()


def controller():
    cursor = mysqldb.cursor()
    query = "SELECT panel_panel_id, rTime FROM reservation"
    cursor.execute(query)
    data = cursor.fetchall()

    now = datetime.now()

    for p_id, result_str in data:
        #p_id = p_id[0]
        #query1 = "SELECT rTime FROM reservation WHERE reservation.panel_panel_id= (%s)"
        #cursor.execute(query1,(p_id,))
        #result = cursor.fetchone()
        
        
        
        
        #result_str = result[0]
        if ':' in result_str:
             
            try:
                result_date = datetime.strptime(result_str,"%H:%M")
                now_time = datetime.strftime(now,"%H:%M")
            
                result_time = result_date.strftime("%H:%M")

                if now_time > result_time :
                    query2 = "DELETE FROM reservation WHERE reservation.panel_panel_id = (%s)"                
                    cursor.execute(query2,(p_id,))

                    panel_update = "UPDATE panel SET rStatus = 'available' WHERE  panel.panel_id =  (%s)"
                    cursor.execute(panel_update,( p_id,))      

            

            except mysql.connector.Error as e:
                        print("Error:", e)
                        mysqldb.rollback()
        elif '.' in result_str:
            try:
                result_date = datetime.strptime(result_str,"%d.%m.%Y")
                today = datetime.strftime(now,"%d.%m.%Y")
                now_day = result_date.strftime("%d.%m.%Y")

                if now_day < today:
                
                    query3 = "DELETE FROM reservation WHERE reservation.panel_panel_id = (%s)"                
                    cursor.execute(query3,(p_id,))

                    panel_update = "UPDATE panel SET rStatus = 'available' WHERE  panel.panel_id = (%s)"
                    cursor.execute(panel_update,( p_id,))

                

            except mysql.connector.Error as e:
                    print("Error:", e)
                    mysqldb.rollback()

        

    cursor.close()





controller()



def add_reservation():
    name = ui.name_edit.text()
    
    panel = ui.panel_edit.text() 
    

    if mysqldb.is_connected:
        print("veritabanına bağlanıldı.")
        
        cursor = mysqldb.cursor()
        control = "SELECT panel.rStatus FROM panel WHERE panel.panel_id = (%s)"
        cursor.execute(control,(panel,))
        result = cursor.fetchone()
        
               


        if result is not None:
            
            

            if "available" == result[0]:

                try:
                
            
            
                    add_user = "INSERT INTO users (name) VALUES (%s)"
                    cursor.execute(add_user,(name,))
                
                    add_panel = "UPDATE panel SET rStatus = 'not available' WHERE  panel.panel_id =  (%s)"
                    cursor.execute(add_panel,(panel,))

                    #rezervasyon yapan kullanıcıyı getir
                    cursor.execute("SELECT LAST_INSERT_ID()")
                    last_inserted_id = cursor.fetchone()[0]
            
                    #rezervasyon yapan kullanıcının adını getir
                    get_user_name_query = "SELECT name FROM users WHERE user_id = %s"
                    cursor.execute(get_user_name_query, (last_inserted_id,))
                    last_inserted_user_name = cursor.fetchone()[0]

                


                
                    add_reservations = "INSERT INTO reservation(users_user_id,panel_panel_id,rTime,rStatus,user_name) VALUES (%s,%s,%s,%s,%s)"
                    cursor.execute(add_reservations,(last_inserted_id,panel,end_time(),"not available",last_inserted_user_name,))

                    

                    #result
                    mysqldb.commit()            
                    list_record()
                    print(" bağlantısı kapatıldı (try blogu).")
                    webhook(name, panel, end_time())
                    ui.name_edit.clear()
                    ui.panel_edit.clear()
                    ui.time_edit.clear()
                    ui.statusbar.showMessage("Reservation successfull ",10000)

                except mysql.connector.Error as e:
                    print("Error:", e)
                    mysqldb.rollback()
                    ui.statusbar.showMessage("Reservation not successfull ",10000)
                finally:
                # Bağlantıyı kapat
                    controller()
                    cursor.close()
                    #mysqldb.close()
                    #print(" bağlantısı kapatıldı")

        
    



            else:
            
                ui.statusbar.showMessage("Unavailable panel! ",10000)

        else:
            ui.statusbar.showMessage("Invalid panel_id! ",10000)


    else:
        print(" veritabanına bağlanılamadı.")




def list_record():
    controller()
    cursor = mysqldb.cursor()
    ui.tableWidget.clear()
    ui.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
    ui.tableWidget.setHorizontalHeaderLabels(("PANEL","STATUS","NAME-SURNAME","END TIME"))
    query = "SELECT reservation.panel_panel_id, reservation.rStatus, reservation.user_name, reservation.rTime FROM reservation INNER JOIN users ON reservation.users_user_id = users.user_id"
    cursor.execute(query)

    for indexRow, reservation_id in enumerate(cursor):
        for indexCol, reservationCol in enumerate(reservation_id):
            ui.tableWidget.setItem(indexRow,indexCol,QTableWidgetItem(str(reservationCol)))
      
    cursor.close()
    
    




def remove_reservation():
    message = QMessageBox.question(window,"Please confirm!","Are you sure you want to remove?")
    QMessageBox.Yes | QMessageBox.No
    cursor = mysqldb.cursor()

    if message == QMessageBox.Yes:
        selected_record = ui.tableWidget.selectedItems()                     

        
            
        try:
            record_to_be_removed = selected_record[0].row()
            item = ui.tableWidget.item(record_to_be_removed, 0)
            item_str = item.text()

            temp_query = "SELECT reservation.users_user_id FROM reservation WHERE reservation.panel_panel_id = (%s)"
            cursor.execute(temp_query,(item_str,))
            result = cursor.fetchone()[0]

            query = "DELETE FROM reservation WHERE reservation.panel_panel_id = (%s)"                
            cursor.execute(query,(item_str,))

            add_panel = "UPDATE panel SET rStatus = 'available' WHERE  panel.panel_id =  (%s)"
            cursor.execute(add_panel,(item_str,))

            remove_user = "DELETE FROM users WHERE users.user_id =(%s)"
            cursor.execute(remove_user,(result,))

            mysqldb.commit()
            ui.statusbar.showMessage("Reservation removed ",10000)
            
            

        except:
            ui.statusbar.showMessage("Reservation not removed ",10000)

        finally:
            # Bağlantıyı kapat
                controller()
                list_record()
                cursor.close()
                #mysqldb.close()
                print("remove bağlantısı kapatıldı")

    

    else:

        ui.statusbar.showMessage("Transaction cancaled",10000)


def end_time():

    try:

        reservation_time_str = ui.time_edit.text()
        reservation_time = int(reservation_time_str)

        now = datetime.now()
        temp = now + timedelta(hours=reservation_time)

        end_time = temp.strftime("%H:%M")

        return end_time
    except:
        day = datetime.today()
        today = datetime.strftime(day,"%d.%m.%Y")
        return today


def search():
    search = ui.search_edit.text()
    ui.search_edit.clear()
    
    if search != "":
        cursor = mysqldb.cursor()
        query = "SELECT reservation.panel_panel_id, reservation.rStatus, reservation.user_name, reservation.rTime FROM reservation WHERE reservation.panel_panel_id = (%s)"
        cursor.execute(query,(search,))
        ui.tableWidget.clear()

        ui.tableWidget.setHorizontalHeaderLabels(("PANEL","STATUS","NAME-SURRNAME","END TIME"))
        for indexRow, reservation_id in enumerate(cursor):
            for indexCol, reservationCol in enumerate(reservation_id):
                ui.tableWidget.setItem(indexRow,indexCol,QTableWidgetItem(str(reservationCol)))
    
        cursor.close()
        controller()

    else:
        controller()
        list_record()
        





        




#butonlar

ui.addButton.clicked.connect(add_reservation)
list_record()
ui.removeButton.clicked.connect(remove_reservation)
ui.searchButton.clicked.connect(search)



def panels():
    
    for i in range(100,121):
        cursor = mysqldb.cursor()
        query = "SELECT COUNT(*) FROM panel WHERE panel_id = %s"
        cursor.execute(query,(i,))
        row_count = cursor.fetchone()[0]

        try:
            if row_count == 0:
                query1 = "INSERT INTO panel (panel_id,rStatus) VALUES (%s,%s)"
                cursor.execute(query1,(i,"available",))
                mysqldb.commit() 
        except mysql.connector.Error as e:
                print("Error:", e)
                mysqldb.rollback()
                    
        finally:
            cursor.close()


def webhook(name,panel,time):
    url ='https://example.webhook.office.com/'
    payload = {
        "title": panel,
        "text" : name + ", " + panel + " panelini " + time + " sonuna kadar rezerve etti."
    }
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    print(response.text.encode('utf8'))






        
    

panels()
controller()
    
sys.exit(app.exec_())  #pencere hemen kapanmasın

