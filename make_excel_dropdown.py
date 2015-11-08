from datetime import date, time
import os
import xlsxwriter

# From
# https://xlsxwriter.readthedocs.org/en/latest/example_data_validate.html

workbook = xlsxwriter.Workbook(os.getenv("HOME")+os.sep+"Downloads"+os.sep+'data_validate.xlsx')
worksheet = workbook.add_worksheet()

# Add a format for the header cells.
header_format = workbook.add_format({
    'border': 1,
    'bg_color': '#C6EFCE',
    'bold': True,
    'text_wrap': True,
    'valign': 'vcenter',
    'indent': 1,
})

# Set up layout of the worksheet.
worksheet.set_column('A:A', 68)
worksheet.set_column('B:B', 20)
worksheet.set_column('C:C', 20)
worksheet.set_column('D:D', 20)
# First row get distance 36
worksheet.set_row(0, 36)

# Write the header cells and some data that will be used in the examples.
heading1 = 'Some examples of data validation in XlsxWriter'
heading2 = 'Enter values in this column'
heading3 = 'Sample Data'

worksheet.write('A1', heading1, header_format)
worksheet.write('B1', heading2, header_format)
worksheet.write('D1', heading3, header_format)

# Put in data, and formulas
worksheet.write_row('D3', ['Integers', 1, 10])
worksheet.write_row('D4', ['List data', 'open', 'high', 'close'])
worksheet.write_row('D5', ['Formula', '=AND(F5=50,G5=60)', 50, 60])


# Example 1. Limiting input to an integer in a fixed range.
txt = 'Enter an integer between 1 and 10'
worksheet.write('A3', txt)
worksheet.data_validation('B3', {'validate': 'integer',
                                 'criteria': 'between',
                                 'minimum': 1,
                                 'maximum': 10})

# Example 2. Limiting input to an integer outside a fixed range.
txt = 'Enter an integer that is not between 1 and 10 (using cell references) in E3 and F3'
worksheet.write('A5', txt)
worksheet.data_validation('B5', {'validate': 'integer',
                                 'criteria': 'not between',
                                 'minimum': '=E3',
                                 'maximum': '=F3'})


# Example 3. Limiting input to an integer greater than a fixed value.
txt = 'Enter an integer greater than 0'
worksheet.write('A7', txt)
worksheet.data_validation('B7', {'validate': 'integer',
                                 'criteria': '>',
                                 'value': 0})

# Example 4. Limiting input to an integer less than a fixed value.
txt = 'Enter an integer less than 10'
worksheet.write('A9', txt)
worksheet.data_validation('B9', {'validate': 'integer',
                                 'criteria': '<',
                                 'value': 10})

# Example 5. Limiting input to a decimal in a fixed range.
txt = 'Enter a decimal between 0.1 and 0.5'
worksheet.write('A11', txt)
worksheet.data_validation('B11', {'validate': 'decimal',
                                  'criteria': 'between',
                                  'minimum': 0.1,
                                  'maximum': 0.5})

# Example 6. Limiting input to a value in a dropdown list.
txt = 'Select a value from a drop down list'
worksheet.write('A13', txt)
worksheet.data_validation('B13', {'validate': 'list',
                                  'source': ['open', 'high', 'close']})

# Example 7. Limiting input to a value in a dropdown list.
txt = 'Select a value from a drop down list (using a cell range) from E4:G4'
worksheet.write('A15', txt)
worksheet.data_validation('B15', {'validate': 'list',
                                  'source': '=$E$4:$G$4'})


# Example 11. Limiting input based on a formula.
txt = 'Enter a value if the following is true "=AND(F5=50,G5=60)"'
worksheet.write('A23', txt)
worksheet.data_validation('B23', {'validate': 'custom',
                                  'value': '=AND(F5=50,G5=60)'})

# Example 14. Conditional double dropdown
EXCEL_LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

l1 =  ['Quiz_1', 'Video_1', 'Video_2']
l2 =  ['Quiz_2', 'Video_3', 'Video_4', 'Video_5']
worksheet.write_row('A32', l1)
worksheet.write_row('A33', l2)
txt = 'Dropdown of quiz and video'
worksheet.write('A36', txt)
txt = 'Dropdown of quiz'
worksheet.write('B35', txt)
txt = 'Dropdown of Video'
worksheet.write('C35', txt)
# Dropdown 1
worksheet.data_validation('B36', {'validate': 'list', 'source': '=A32:A33'})
# Dropdown 2 dependent on dropdown 2
worksheet.data_validation('C36', {'validate': 'list', 'source': '=IF(B36=A32, B32:C32, IF(B36=A33, B33:D33, "NIL"))'})

# Example 15. List of lists
vids = [['Quiz_3', 'Video_6', 'Video_7'], ['Quiz_4', 'Video_8', 'Video_9', 'Video_10'], ['Quiz_5', 'Video_11', 'Video_12', 'Video_13', 'Video_14']]

start = 'A40'
col_s = start[0]
row_s = int(start[1:])

# Write all options
dic = {}
for i, vid in enumerate(vids):
    cr = col_s+str(row_s+i)
    worksheet.write_row(cr, vid)
    dic[str(i)] = {}
    dic[str(i)]['cr'] = cr
    dic[str(i)]['col'] = col_s
    col_nr = EXCEL_LETTERS.index(col_s.upper())
    dic[str(i)]['row'] = row_s+i
    dic[str(i)]['len'] = len(vid)
    dic[str(i)]['quiz_cr'] = EXCEL_LETTERS[col_nr]+str(row_s+i)
    dic[str(i)]['video_crs'] = "%s%s:%s%s"%(EXCEL_LETTERS[col_nr+1], str(row_s+i), EXCEL_LETTERS[col_nr+len(vid)-1], str(row_s+i))
    dic[str(i)]['quiz_videos'] = vid
    dic['nr_quiz_videos'] = i+1

# Write header cells
c_h1 = "A"
c_h2 = "B"
c_h3 = "C"
dist = 2
worksheet.write(c_h1+str(dic[str(dic['nr_quiz_videos']-1)]['row']+dist), "Name of quiz", header_format)
worksheet.write(c_h2+str(dic[str(dic['nr_quiz_videos']-1)]['row']+dist), "Dropdown of quiz", header_format)
worksheet.write(c_h3+str(dic[str(dic['nr_quiz_videos']-1)]['row']+dist), "Dropdown of Video", header_format)

# Write first
nr_questions = 10
for j in range(nr_questions):
    cdist = dist + 1 + j
    worksheet.write(c_h1+str(dic[str(dic['nr_quiz_videos']-1)]['row']+cdist), "Quiz %i"%j)

    # Get position
    quiz_cr = c_h2+str(dic[str(dic['nr_quiz_videos']-1)]['row']+cdist)
    worksheet.data_validation(quiz_cr, {'validate': 'list', 'source': '=%s:%s'%(dic['0']['cr'], dic[str(dic['nr_quiz_videos']-1)]['cr'])})

# Make chained else if command
for j in range(nr_questions):
    cdist = dist + 1 + j
    quiz_cr = c_h2+str(dic[str(dic['nr_quiz_videos']-1)]['row']+cdist)
    video_cr = c_h3+str(dic[str(dic['nr_quiz_videos']-1)]['row']+cdist)

    # Make chain
    astr = "="
    estr = ""
    for k in range(dic['nr_quiz_videos']):
        cstr = "IF(%s=%s, %s, "%(quiz_cr, dic[str(k)]['quiz_cr'], dic[str(k)]['video_crs'])
        astr = astr + cstr
        estr = estr + ")"

        if k == dic['nr_quiz_videos']-1:
            estr = '"NIL"' + estr

    chain_str = astr + estr
    worksheet.data_validation(video_cr, {'validate': 'list', 'source': chain_str})

# Close workbook
workbook.close()


