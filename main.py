import math

class Placement:
    """Класс для хранения параметров расчёта укладки клиновых кирпичей"""
    
    def __init__(self, bricks_count, bricks1_face, bricks2_face):
        self.bricks_count = bricks_count
        self.bricks1_face = min(bricks1_face, bricks2_face)  # Лицевая сторона кирпича типа 1 (мм)
        self.bricks2_face = max(bricks1_face, bricks2_face)  # Лицевая сторона кирпича типа 2 (мм)

    def calculate_optimal_placement(self, inner_diameter_mm):
        """Расчёт оптимального количества и соотношения кирпичей"""
        
        if self.bricks1_face == self.bricks2_face:
            raise ValueError("Размеры кирпичей должны быть разными для расчёта")
        
        L_inner = math.pi * inner_diameter_mm
        
        # Ищем оптимальное соотношение, стремясь к 1:1
        best_N = None
        best_ratio = float('inf')
        best_diff = float('inf')
        best_x = 0
        
        for N in range(self.bricks_count - 1, self.bricks_count + 1):
            # Находим оптимальное количество кирпичей типа 2 для данного общего количества
            x = int(math.ceil((self.bricks2_face * N - L_inner) / abs(self.bricks1_face - self.bricks2_face)))

            
            if x < 0 or x > N:
                continue
                
            L_inner_brics = self.bricks1_face * x + self.bricks2_face * (N - x)
            diff = abs(L_inner - L_inner_brics)
            
            # Выбираем решение с минимальным отклонением и соотношением ближе к 1:1
            if (diff < best_diff or 
                (abs(diff - best_diff) < 0.1 and abs(self.bricks2_face / self.bricks1_face - 1) < abs(best_ratio - 1))):
                best_N = N
                best_ratio = x / max(N - x, 1)
                best_diff = diff
                best_x = x
        
        return {
            'N': best_N,
            'ratio': best_ratio,
            'diff_mm': round(best_diff),
            'x_type1': best_x,
            'x_type2': best_N - best_x if best_N else 0
        }


def main():
    """Основная функция программы"""
    
    print("=" * 60)
    print("Расчёт оптимальной укладки клиновых кирпичей в трубу")
    print("=" * 60)
    
    # Ввод данных с проверкой на корректность
    try:
        D_outer = float(input('Введи диаметр трубы (мм): '))
        
        if D_outer <= 0:
            raise ValueError("Диаметр должен быть положительным")
        
        bricks_height = float(input('Введи высоту/толщину кирпича (мм): '))
        
        if bricks_height <= 0:
            raise ValueError("Высота должна быть положительной")
        
        bricks_back = float(input('Введи жопу кирпича (мм): '))
        
        if bricks_back <= 0:
            raise ValueError("Жопа должна быть положительной")
        
        brick1_face, brick2_face = map(float, input('Введи морды кирпичей через пробел (например: 50 60): ').split())
        
        if brick1_face <= 0 or brick2_face <= 0:
            raise ValueError("Морды должны быть положительными")
            
    except ValueError as e:
        print(f"Ошибка ввода: {e}")
        return
    
    # Проверка на возможность размещения кирпичей в трубе
    D_inner = D_outer - 2 * bricks_height
    
    if D_inner <= 0:
        print('❌ Кирпичи не поместятся в трубу (толщина кирпича слишком большая).')
        return
    
    # Расчёт длины окружностей
    L_outer = math.pi * D_outer
    L_inner = math.pi * D_inner
    
    bricks_av = round(L_outer / bricks_back)
    
    print(f"\n📐 Внутренний диаметр трубы: {D_inner:.2f} мм")
    print(f"📏 Длина внутренней окружности: {L_inner:.2f} мм")
    print(f"🧱 Ожидаемое количество кирпичей по глубине: ~{bricks_av}")
    
    # Создание объекта Placement и расчёт оптимального решения
    placement = Placement(bricks_av, brick1_face, brick2_face)
    result = placement.calculate_optimal_placement(D_inner)
    
    if result['N'] is None:
        print('⚠️ Не удалось найти оптимальное решение. Попробуйте другие размеры кирпичей.')
        return
    
    # Вывод результатов
    print("\n" + "=" * 60)
    print("📊 РЕЗУЛЬТАТЫ РАСЧЁТА")
    print("=" * 60)
    
    print(f"✅ Оптимальное число кирпичей: {result['N']}")
    print(f"   — Кирпичи типа 1 (размер {brick1_face} мм): {result['x_type1']} шт.")
    print(f"   — Кирпичи типа 2 (размер {brick2_face} мм): {result['x_type2']} шт.")
    
    if result['N'] > 0:
        ratio_str = f"{result['ratio']:.2f}"
        print(f"📈 Соотношение кирпичей 1 к 2: {ratio_str}")
        
        # Оценка близости к идеалу 1:1
        ideal_ratio = 1.0
        deviation = abs(result['ratio'] - ideal_ratio) * 100
        if deviation < 50:
            print(f"   💚 Отклонение от идеала (1:1): {deviation:.1f}%")
        else:
            print(f"   ⚠️  Значительное отклонение от идеала (1:1)")
    
    print(f"📏 Допуск при укладке: {result['diff_mm']} мм")
    
    while True:
        continue
   
main()