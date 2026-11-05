#умный дневник кбжу с учетом цели
#автор: Дарыбаева Розалина Азаматовна

user_profile = {}
daily_norms = {}
food_log = []


def calculate_norms(gender, age, height, weight, activity, goal):
    """расчет нормы кбжу с учетом цели. 1 - похудение, 2 - поддержание, 3 - набор массы"""
    #базовый метаболизм 
    if gender.lower() in ['м', 'муж', 'мужской', 'm']:
        bmr = 10 * weight + 6.25 * height - 5 * age + 5
    else:
        bmr = 10 * weight + 6.25 * height - 5 * age - 161

    #коэффициент активности
    activity_multipliers = {1: 1.2, 2: 1.375, 3: 1.55, 4: 1.725, 5: 1.9}
    mult = activity_multipliers.get(activity, 1.375)
    
    base_kcal = bmr * mult

    #корректировка под цель
    if goal == 1:
        #похудение- минус 15% калорий
        total_kcal = round(base_kcal * 0.85)
    elif goal == 3:
        #набор массы- плюс 15% калорий
        total_kcal = round(base_kcal * 1.15)
    else:
        #поддержание- без изменений
        total_kcal = round(base_kcal)

    #расчет БЖУ
    #белки= 2.2г на 1кг веса
    protein_norm = round(weight * 2.2)
    #жиры= 1.4г на 1кг веса
    fat_norm = round(weight * 1.4)
    
    #угли= оставшиеся калории
    carb_calories = total_kcal - (protein_norm * 4 + fat_norm * 9)
    
    #защита от отрицательных углеводов
    if carb_calories < 0:
        carb_norm = 0
    else:
        carb_norm = round(carb_calories / 4)

    return {
        "kcal": total_kcal,
        "protein": protein_norm,
        "fat": fat_norm,
        "carbs": carb_norm
    }


def setup_profile():
    """спрашивает данные у пользователя и сохраняет нормы."""
    global user_profile, daily_norms
    print("\nНАСТРОЙКА ПРОФИЛЯ")
    
    gender = input("Твой пол (м/ж): ").strip()
    age = input_float("Возраст (лет): ")
    height = input_float("Рост (см): ")
    weight = input_float("Вес (кг): ")
    
    print("\nУровень активности:")
    print("1. Минимальный (сидячая работа)")
    print("2. Легкий (тренировки 1-3 раза в неделю)")
    print("3. Средний (тренировки 3-5 раз в неделю)")
    print("4. Высокий (тренировки 6-7 раз в неделю)")
    print("5. Экстремальный (тяжелый физический труд)")
    activity = int(input_float("Выбери пункт (1-5): "))
    
    print("\nТвоя цель:")
    print("1. Похудение")
    print("2. Поддержание веса")
    print("3. Набор массы")
    goal = int(input_float("Выбери пункт (1-3): "))
    
    user_profile = {"gender": gender, "age": age, "height": height, "weight": weight, "goal": goal}
    daily_norms = calculate_norms(gender, age, height, weight, activity, goal)
    
    goal_names = {1: "Похудение", 2: "Поддержание", 3: "Набор массы"}
    print(f"\n--- ТВОЯ ЦЕЛЬ: {goal_names.get(goal, 'Поддержание').upper()} ---")
    print(f"Твоя дневная норма:")
    print(f"Калории: {daily_norms['kcal']} ккал")
    print(f"Белки: {daily_norms['protein']} г")
    print(f"Жиры: {daily_norms['fat']} г")
    print(f"Углеводы: {daily_norms['carbs']} г")


def calculate_macros(kcal_100, prot_100, fat_100, carb_100, weight):
    """считает КБЖУ на основе данных на 100г и веса порции."""
    factor = weight / 100
    return {
        "kcal": round(kcal_100 * factor),
        "protein": round(prot_100 * factor, 1),
        "fat": round(fat_100 * factor, 1),
        "carbs": round(carb_100 * factor, 1)
    }


def add_food(name, weight, macros):
    """Добавляет продукт в дневник."""
    if not name.strip() or weight <= 0:
        return False
    entry = {"name": name.strip(), "weight": weight}
    entry.update(macros)
    food_log.append(entry)
    return True


def get_totals():
    """Считает сумму КБЖУ за день."""
    totals = {"kcal": 0, "protein": 0.0, "fat": 0.0, "carbs": 0.0}
    for item in food_log:
        for key in totals:
            totals[key] += item[key]
    
    totals["kcal"] = round(totals["kcal"])
    totals["protein"] = round(totals["protein"], 1)
    totals["fat"] = round(totals["fat"], 1)
    totals["carbs"] = round(totals["carbs"], 1)
    return totals


def show_log():
    """Печатает список продуктов и остаток до нормы."""
    if not food_log:
        print("\nСегодня ещё ничего не съедено.")
        return
    
    print("\nСъедено сегодня")
    for item in food_log:
        print(f"{item['name']} ({item['weight']}г): {item['kcal']} ккал | Б:{item['protein']} Ж:{item['fat']} У:{item['carbs']}")
    
    totals = get_totals()
    print("\nИтого за день")
    print(f"Калории: {totals['kcal']} / {daily_norms['kcal']} ккал")
    print(f"Белки: {totals['protein']} / {daily_norms['protein']} г")
    print(f"Жиры: {totals['fat']} / {daily_norms['fat']} г")
    print(f"Углеводы: {totals['carbs']} / {daily_norms['carbs']} г")
    
    left_kcal = daily_norms['kcal'] - totals['kcal']
    if left_kcal >= 0:
        print(f"\nОсталось съесть: {left_kcal} ккал")
    else:
        print(f"\nПеребор на {-left_kcal} ккал!")


def show_menu():
    """Печатает главное меню."""
    print("\nГлавное меню")
    print("1. Добавить продукт в дневник")
    print("2. Показать дневник за день")
    print("3. Калькулятор блюда (посчитать КБЖУ)")
    print("4. Изменить профиль / цель (пересчитать)")
    print("5. Очистить дневник")
    print("0. Выход")


def input_float(prompt):
    """Вспомогательная функция для безопасного ввода чисел."""
    while True:
        raw = input(prompt).replace(',', '.').strip()
        try:
            val = float(raw)
            if val < 0:
                print("Значение не может быть отрицательным.")
                continue
            return val
        except ValueError:
            print("Ошибка: нужно ввести число (например, 150 или 12.5).")


def main():
    print("Умный дневник кбжу")
    setup_profile()
    
    while True:
        show_menu()
        choice = input("Выбери пункт: ").strip()

        if choice == "1":
            name = input("Название продукта: ")
            weight = input_float("Вес порции (в граммах): ")
            
            print("Введи КБЖУ на 100 грамм (если не знаешь, введи 0):")
            kcal_100 = input_float("  Калории: ")
            prot_100 = input_float("  Белки: ")
            fat_100 = input_float("  Жиры: ")
            carb_100 = input_float("  Углеводы: ")

            macros = calculate_macros(kcal_100, prot_100, fat_100, carb_100, weight)
            
            if add_food(name, weight, macros):
                print(f"'{name}' ({weight}г) добавлено в дневник.")
            else:
                print("Ошибка добавления (пустое имя или неверный вес).")

        elif choice == "2":
            show_log()

        elif choice == "3":
            print("\nКалькулятор блюда")
            weight = input_float("Вес порции (в граммах): ")
            kcal_100 = input_float("Калории на 100г: ")
            prot_100 = input_float("Белки на 100г: ")
            fat_100 = input_float("Жиры на 100г: ")
            carb_100 = input_float("Углеводы на 100г: ")
            
            result = calculate_macros(kcal_100, prot_100, fat_100, carb_100, weight)
            print(f"\nРезультат для порции {weight}г:")
            print(f"Ккал: {result['kcal']} | Б: {result['protein']} | Ж: {result['fat']} | У: {result['carbs']}")

        elif choice == "4":
            setup_profile()

        elif choice == "5":
            count = len(food_log)
            food_log.clear()
            print(f"Дневник очищен. Удалено записей: {count}.")

        elif choice == "0":
            print("До встречи!")
            break
        else:
            print("Нет такого пункта. Введи число из меню.")

        input("\nНажми Enter, чтобы продолжить.")


if __name__ == "__main__":
    main()