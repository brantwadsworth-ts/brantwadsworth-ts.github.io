from flask import Flask, request, send_file, render_template
from datetime import datetime, timedelta
import csv

app = Flask(__name__)

def generate_calendar(fiscal_start_date, fiscal_end_date, calendar_type, quarter_prefix, fiscal_year_prefix, start_day_of_week):
    date_data = []
    current_date = fiscal_start_date

    year = int(fiscal_start_date.strftime('%Y'))
    first_day_of_year = datetime(fiscal_start_date.year, 1, 1)
    quarter_m1 = 4
    quarter_m2 = 5
    quarter_m3 = 4

    if current_date > first_day_of_year:
        year += 1

    quarter = 1
    adjusted_weekday_number = 1
    day_number_of_month = 0
    day_number_of_quarter = 0
    day_number_of_year = 0
    week_of_month = 0
    week_of_quarter = 0
    week_of_year = 0
    month_number_of_quarter = 1
    month_number_of_year = 1

    while current_date <= fiscal_end_date:
        date = current_date.strftime('%Y-%m-%d')
        absolute_week_number = current_date.strftime('%W')
        weekday_name = current_date.strftime('%A')
        is_weekend = 'Yes' if current_date.strftime('%w') in ['0', '6'] else 'No'
        weekday_number = current_date.weekday()

        if start_day_of_week == 1:  # Sunday
            day_number_of_month += 1
            day_number_of_quarter += 1
            day_number_of_year += 1

            if weekday_number == 6:  # Sunday
                adjusted_weekday_number = 1
                start_of_week_epoch = current_date.strftime('%Y-%m-%d')
                end_of_week_epoch = (current_date + timedelta(days=6 - current_date.weekday())).strftime('%Y-%m-%d')

                if week_of_year < 53 and weekday_number == 6:
                    week_of_year += 1
                    week_of_quarter += 1
                    week_of_month += 1

                    if week_of_quarter <= 13:
                        if week_of_quarter == quarter_m1 + 1:
                            day_number_of_month = 1
                            week_of_month = 1
                            month_number_of_quarter = 2
                            month_number_of_year += 1
                            month = current_date.strftime('%B')

                        elif week_of_quarter == quarter_m2 + 1:
                            day_number_of_month = 1
                            week_of_month = 1
                            month_number_of_quarter = 3
                            month_number_of_year += 1
                            month = current_date.strftime('%B')

                        elif week_of_quarter == quarter_m3 + 1:
                            quarter += 1
                            day_number_of_month = 1
                            week_of_month = 1
                            month_number_of_quarter = 1
                            month_number_of_year += 1
                            month = current_date.strftime('%B')

                        elif week_of_quarter == 1:
                            month = current_date.strftime('%B')

                else:
                    quarter += 1
                    month_number_of_quarter = 1
                    week_of_quarter = 1
                    week_of_month = 1
                    day_number_of_month = 1
                    day_number_of_quarter = 1
                    month = current_date.strftime('%B')

            elif weekday_number == 6:
                week_of_year = 1
                year += 1

        else:
            adjusted_weekday_number = weekday_number + 2

        quarter_fiscal = quarter_prefix + str(quarter)
        year_fiscal = fiscal_year_prefix + str(year)

        date_data.append([
            date, weekday_name, adjusted_weekday_number, month, quarter_fiscal, year_fiscal,
            week_of_month, week_of_quarter, week_of_year, is_weekend, day_number_of_month,
            day_number_of_quarter, day_number_of_year, month_number_of_quarter,
            month_number_of_year, absolute_week_number, start_of_week_epoch, end_of_week_epoch
        ])

        current_date += timedelta(days=1)

    return date_data

def write_to_csv(filename, data):
    with open(filename, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow([
            'date', 'weekday_name', 'day_of_week', 'month', 'quarter', 'year',
            'week_number_of_month', 'week_number_of_quarter', 'week_number_of_year',
            'is_weekend', 'day_number_of_month', 'day_number_of_quarter', 'day_number_of_year',
            'month_number_of_quarter', 'month_number_of_year', 'absolute_week_number',
            'start_of_week_epoch', 'end_of_week_epoch'
        ])
        csv_writer.writerows(data)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate-calendar', methods=['POST'])
def generate_calendar_route():
    fiscal_start_date = datetime.strptime(request.form['fiscal_start_date'], '%Y-%m-%d')
    fiscal_end_date = datetime.strptime(request.form['fiscal_end_date'], '%Y-%m-%d')
    calendar_type = request.form['calendar_type']
    quarter_prefix = request.form['quarter_prefix']
    fiscal_year_prefix = request.form['fiscal_year_prefix']
    start_day_of_week = int(request.form['start_day_of_week'])

    date_data = generate_calendar(fiscal_start_date, fiscal_end_date, calendar_type, quarter_prefix, fiscal_year_prefix, start_day_of_week)

    filename = f'{calendar_type}_calendar.csv'
    write_to_csv(filename, date_data)

    return send_file(filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
