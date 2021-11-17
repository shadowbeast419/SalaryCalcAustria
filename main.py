"""
Gross/net calculator
Austria, 2021

(c) Christoph alias shadowbeast, gidof

Just joking, no copyright whatsoever. However, feedback is always welcome!


"""

import numpy as np
import matplotlib.pyplot as plt

"""
CONSTANTS
"""

full_time_hours = 38.5

# not taxed, 12 times a year
monthly_benefits = 160.0

# used for x-Axes
max_x_salary = 4000

# for manual calculation
part_time_hours = 16.0

# for manual calculation
# including monthly benefits
target_monthly_net_salary = 1200

# 2021
# https://www.finanz.at/steuern/lohnsteuertabelle/
income_tax_levels = np.array([[9999999999, 83349.33, 55],
                            [83349.33, 7516, 50],
                            [7516, 5016, 48],
                            [5016, 2599.33, 42],
                            [2599.33, 1516, 35],
                            [1516, 1099.33, 20]])


# Insurance tax does really only depend on thresholds
def insurance_tax(gross_salary):
    if gross_salary < 478.81:
        insurance_tax_percent = 0.0
    elif 478.81 <= gross_salary < 1790.0:
        insurance_tax_percent = 15.12
    elif 1790.0 <= gross_salary < 1953.0:
        insurance_tax_percent = 16.12
    elif 1953.0 <= gross_salary < 2117.0:
        insurance_tax_percent = 17.12
    elif 2117.0 <= gross_salary < 5550:
        insurance_tax_percent = 18.12
    # > 5500 Euro -> constant amount
    else:
        return 1005.66

    return gross_salary * insurance_tax_percent / 100.0


def holiday_insurance_tax(gross_salary):
    if gross_salary < 475.86:
        holiday_salary_tax_percent = 0.0
    elif gross_salary < 1790.0:
        holiday_salary_tax_percent = 14.12
    elif gross_salary < 1953.0:
        holiday_salary_tax_percent = 15.12
    elif gross_salary < 2117.0:
        holiday_salary_tax_percent = 16.12
    elif gross_salary < 5550:
        holiday_salary_tax_percent = 17.12
    # > 5500 Euro -> constant amount
    else:
        return 1900.32

    return gross_salary * holiday_salary_tax_percent / 100.0


# Does not affect the whole gross income -> insurance taxes are not taken into account
# Percentage only affects the amount over the certain threshold
def income_tax(gross_salary_monthly):

    # insurance tax is tax free
    gross_salary_annually = gross_salary_monthly * 14 - \
                            12 * insurance_tax(gross_salary_monthly) - 2 * holiday_insurance_tax(gross_salary_monthly)

    gross_salary_monthly_taxfree = gross_salary_annually / 14

    income_tax_monthly = 0

    # > 83344.33
    if gross_salary_monthly_taxfree > income_tax_levels[0, 1]:
        income_tax_percent = income_tax_levels[0, 2]

        tax_class_diff = gross_salary_monthly_taxfree - income_tax_levels[0, 1]
        # only everything about the threshold will be taxed
        income_tax_monthly += (tax_class_diff * income_tax_percent / 100.0)

        # calculate further with the rest for the next tax class
        gross_salary_monthly_taxfree = income_tax_levels[0, 1]

    #  7516 < salary < 8334433
    if gross_salary_monthly_taxfree >= income_tax_levels[1, 1]:
        income_tax_percent = income_tax_levels[1, 2]

        tax_class_diff = gross_salary_monthly_taxfree - income_tax_levels[1, 1]
        income_tax_monthly += (tax_class_diff * income_tax_percent / 100.0)
        gross_salary_monthly_taxfree -= tax_class_diff

    #  5016 < salary < 7516
    if gross_salary_monthly_taxfree >= income_tax_levels[2, 1]:
        income_tax_percent = income_tax_levels[2, 2]

        tax_class_diff = gross_salary_monthly_taxfree - income_tax_levels[2, 1]
        income_tax_monthly += (tax_class_diff * income_tax_percent / 100.0)
        gross_salary_monthly_taxfree -= tax_class_diff

    #  31.000 < salary < 60.000
    if gross_salary_monthly_taxfree >= income_tax_levels[3, 1]:
        income_tax_percent = income_tax_levels[3, 2]

        tax_class_diff = gross_salary_monthly_taxfree - income_tax_levels[3, 1]
        income_tax_monthly += (tax_class_diff * income_tax_percent / 100.0)
        gross_salary_monthly_taxfree -= tax_class_diff

    #  5.011,00 < salary < 7.511,00
    if gross_salary_monthly_taxfree >= income_tax_levels[4, 1]:
        income_tax_percent = income_tax_levels[4, 2]

        tax_class_diff = gross_salary_monthly_taxfree - income_tax_levels[4, 1]
        income_tax_monthly += (tax_class_diff * income_tax_percent / 100.0)
        gross_salary_monthly_taxfree -= tax_class_diff

    #  2.594,33 < salary < 5.011,00
    if gross_salary_monthly_taxfree >= income_tax_levels[5, 1]:
        income_tax_percent = income_tax_levels[5, 2]

        tax_class_diff = gross_salary_monthly_taxfree - income_tax_levels[5, 1]
        income_tax_monthly += (tax_class_diff * income_tax_percent / 100.0)
        gross_salary_monthly_taxfree -= tax_class_diff

    return income_tax_monthly


# income taxes for 13. and 14. salary
def holiday_income_tax(gross_salary_monthly):
    # "Bagatellgrenze" -> 2100 Euro for 13. & 14 salary are tax free
    gross_holiday_salary = gross_salary_monthly * 2 - 2100.0

    if gross_holiday_salary < 0:
        return 0.0

    holiday_salary_tax = 0.0

    # > 83333
    if gross_holiday_salary > 83333:
        holiday_income_tax_percent = 50.0

        tax_class_diff = gross_holiday_salary - 1000000.0
        # only everything about the threshold will be taxed
        holiday_salary_tax += (tax_class_diff * holiday_income_tax_percent / 100.0)

        # calculate further with the rest for the next tax class
        gross_holiday_salary -= tax_class_diff

    #  83.333 < salary < 50.000
    if gross_holiday_salary >= 50000.0:
        holiday_income_tax_percent = 35.75

        tax_class_diff = gross_holiday_salary - 50000.0
        holiday_salary_tax += (tax_class_diff * holiday_income_tax_percent / 100.0)
        gross_holiday_salary -= tax_class_diff

    #  50.000 < salary < 25.000
    if gross_holiday_salary >= 25000.0:
        holiday_income_tax_percent = 27.0

        tax_class_diff = gross_holiday_salary - 25000.0
        holiday_salary_tax += (tax_class_diff * holiday_income_tax_percent / 100.0)
        gross_holiday_salary -= tax_class_diff

    #  25.000 < salary < 620
    if gross_holiday_salary >= 620.0:
        holiday_income_tax_percent = 6.0

        tax_class_diff = gross_holiday_salary - 620.0
        holiday_salary_tax += (tax_class_diff * holiday_income_tax_percent / 100.0)
        gross_holiday_salary -= tax_class_diff

    return holiday_salary_tax


def calculate_annual_net_salary_and_taxes(gross_monthly_income):
    gross_yearly_income = gross_monthly_income * 14

    income_tax_monthly = income_tax(gross_monthly_income)
    holiday_income_tax_monthly = holiday_income_tax(gross_monthly_income) * 2

    insurance_tax_monthly = insurance_tax(gross_monthly_income)
    holiday_insurance_tax_monthly = holiday_insurance_tax(gross_monthly_income)

    income_tax_sum = income_tax_monthly * 12 + holiday_income_tax_monthly * 2
    insurance_tax_yearly = insurance_tax_monthly * 12 + holiday_insurance_tax_monthly * 2

    net_yearly_income = gross_yearly_income - income_tax_sum - insurance_tax_yearly

    return np.array([gross_yearly_income, income_tax_sum, insurance_tax_yearly, net_yearly_income])


def calculate_net_hourly_salary_from_gross(gross_monthly_income):
    net_salary_annually = calculate_annual_net_salary_and_taxes(gross_monthly_income)[3]
    weeks_per_month = 4.34524

    return net_salary_annually / 12.0 / weeks_per_month / full_time_hours


def main_func():

    gross_salary = np.linspace(0, max_x_salary, 100)
    statistics_matrix = np.zeros((gross_salary.size, 4))

    for i in range(gross_salary.size):
        statistics_matrix[i, :] = np.array(calculate_annual_net_salary_and_taxes(gross_salary[i]))

    plt.figure(0)
    fig, axs = plt.subplots(2, 1)
    fig.set_dpi(200)
    fig.suptitle('Austria 2021 Gross/Net Salary Overview (14 monthly salaries)')

    axs[0].set_xlabel('Monthly gross income full-time [EUR/month]')
    axs[0].set_ylabel('Yearly salary [EUR/year]')

    axs[0].plot(gross_salary, statistics_matrix[:, 0], 'r', label='Annual gross salary')
    axs[0].plot(gross_salary, statistics_matrix[:, 1], 'c', label='Annual income tax', linestyle='dashed')
    axs[0].plot(gross_salary, statistics_matrix[:, 2], 'b', label='Annual insurance tax', linestyle='dotted')
    axs[0].plot(gross_salary, statistics_matrix[:, 3], 'g', label='Annual net salary')
    axs[0].legend(loc='upper left')

    salary_vector = np.zeros(gross_salary.size)

    for i in range(gross_salary.size):
        salary_vector[i] = calculate_net_hourly_salary_from_gross(gross_salary[i])

    axs[1].set_xlabel('Monthly gross income full-time [EUR/month]')
    axs[1].set_ylabel('Net income/hour [EUR/h]')
    axs[1].plot(gross_salary, salary_vector, 'g')

    plt.tight_layout()
    plt.show()

    # show the plot
    fig2 = plt.figure(1)
    fig2.set_dpi(250)
    ax = plt.axes(projection='3d')

    hour_vector = np.linspace(0, full_time_hours * 1.5, gross_salary.size)
    X, Y = np.meshgrid(gross_salary, hour_vector)

    Z = np.zeros((gross_salary.size, hour_vector.size))

    for x in range(gross_salary.size):
        for y in range(hour_vector.size):
            Z[x][y] = calculate_net_hourly_salary_from_gross(gross_salary[x]) * (hour_vector[y] * 4.34524)

            if Z[x][y] + monthly_benefits > target_monthly_net_salary and hour_vector[y] <= part_time_hours:
                print('Gross salary for ' + str(target_monthly_net_salary) + ' net with '
                      + str(part_time_hours) + ' hours: ' + str(gross_salary[x]))

    ax.set_xlabel('Monthly gross income full-time [Euro/month]')
    ax.set_ylabel('Working hours [h]')
    ax.set_zlabel('Monthly net income [Euro/month]')

    ax.contour3D(X, Y, Z, 50, cmap='inferno')

    plt.tight_layout()
    plt.show()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main_func()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
