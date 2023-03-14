@app.route('/get_row_data_2', methods=['POST'])
# def get_row_data_2():
#         conn = sqlite3.connect('.\database\database.db')
#         cursor = conn.cursor()
#         selected_value_2 = request.form['selected_value_2']
#         print(selected_value_2)
#         cursor.execute("SELECT * FROM phone WHERE  \ufeffPhone_name = ?", (selected_value_2,))
#         row_data_2 = cursor.fetchone()
#         response_2 = {'column_1': row_data_2[0], 'column_2': row_data_2[1], 'column_3': row_data_2[2], 'column_4': row_data_2[3], 'column_5': row_data_2[5],
#                  'column_6': row_data_2[6], 'column_7': row_data_2[7], 'column_8': row_data_2[8], 'column_9': row_data_2[9], 'column_10': row_data_2[10], 
#                  'column_11': row_data_2[11]}
#         return jsonify(response_2)