import tkinter as tk
from os import stat_result
from tkinter import ttk
from standards.gost import gost
from standards.iso import iso
from standards.vdz import vdz
from math import pi, ceil

STANDARDS = {
    "ГОСТ": gost,
    "ISO": iso,
    "VDZ": vdz,
}

def validate_values(format_1_name, format_2_name, D_outer, L):
    if format_1_name == format_2_name:
        raise Exception("Футеровку нужно складывать из 2ух разных фороматов")

    try:
        d = float(D_outer)
        if not d.is_integer():
            raise Exception("Диаметр должен быть целым числом")
        if d <= 0:
            raise Exception("Диаметр должен быть положительным")
    except ValueError:
        raise Exception("Введи корректный диаметр")

    try:
        l = float(L)
        if l<=0:
            raise Exception("Длинна печи должна быть положительной")
    except ValueError:
        raise Exception("Введи корректную длинну печи")

def render_result(result_str):
    result_text.configure(state="normal")
    result_text.delete("1.0", tk.END)
    result_text.insert(tk.END, result_str)
    result_text.configure(state="disabled")


def update_formats(event=None):
    selected_standard = standard_select.get()
    data = STANDARDS.get(selected_standard, {})

    values = list(data.keys())

    first_format["values"] = values
    second_format["values"] = values

    if values:
        first_format.current(0)
        second_format.current(1)
    else:
        first_format.set("")
        second_format.set("")


def calc(selected_standard, format_1_name, format_2_name, d_outer, l_furnace):
    data = STANDARDS[selected_standard]

    brick_1 = data[format_1_name] if format_1_name in data else data[int(format_1_name)]
    brick_2 = data[format_2_name] if format_2_name in data else data[int(format_2_name)]

    if brick_1['c'] != brick_2['c']:
        return "Высоты форматов не совпадают. Выбери сопоставимые форматы."

    if brick_1['b'] != brick_2['b']:
        return "Длины кирпичей не совпадают. Выбери сопоставимые форматы"

    brick_height = brick_1['c']
    brick_l = brick_1['b']
    d_inner = d_outer - 2*brick_height
    l_outer = d_outer*pi
    l_inner = d_inner*pi
    brick2_n_raw = ((l_inner-(brick_1['a1']/brick_1['a'])*l_outer)/(brick_2['a1']-(brick_1['a1']/brick_1['a'])*brick_2['a']))
    brick1_n_raw = (l_outer-brick2_n_raw*brick_2['a'])/brick_1['a']
    brick2_n = round(brick2_n_raw)
    brick1_n = round(brick1_n_raw)
    return (f"🧱 Кирпичей в кольце {brick1_n + brick2_n}. Из них:\n"
            f"===================\n"            
            f"{brick1_n} кирпичей {selected_standard} {format_1_name}\n"
            f"{brick2_n} кирпичей {selected_standard} {format_2_name}\n"
            f"===================\n"
            f"Количество колец: {ceil(l_furnace/brick_l)}")


def submit():
    selected_standard = standard_select.get()
    format_1_name = first_format.get()
    format_2_name = second_format.get()
    D_outer_raw = furnace_D.get()
    L_raw = furnace_L.get()

    try:
        validate_values(format_1_name, format_2_name, D_outer_raw, L_raw)
    except Exception as e:
        render_result(str(e))

    d_outer = int(D_outer_raw)
    l = float(L_raw)*1000

    try:
        render_result(calc(selected_standard, format_1_name, format_2_name, d_outer, l))
    except Exception as e:
        render_result(str(e))

root = tk.Tk()
root.title("Расчёт футеровки клиновым кирпичем")
root.geometry("800x450")


main_frame = ttk.Frame(root, padding=20)
main_frame.pack(fill=tk.BOTH, expand=True)

selectors_frame = ttk.Frame(main_frame)
selectors_frame.pack(fill=tk.X)

ttk.Label(selectors_frame, text="Стандарт").grid(row=0, column=0, sticky="w")
standard_select = ttk.Combobox(
    selectors_frame,
    values=list(STANDARDS.keys()),
    state="readonly"
)
standard_select.grid(row=1, column=0, padx=(0, 15), sticky="ew")
standard_select.current(0)
standard_select.bind("<<ComboboxSelected>>", update_formats)

ttk.Label(selectors_frame, text="Формат 1").grid(row=0, column=1, sticky="w")
first_format = ttk.Combobox(selectors_frame, values=[], state="readonly")
first_format.grid(row=1, column=1, padx=(0, 15), sticky="ew")

ttk.Label(selectors_frame, text="Формат 2").grid(row=0, column=2, sticky="w")
second_format = ttk.Combobox(selectors_frame, values=[], state="readonly")
second_format.grid(row=1, column=2, padx=(0, 15), sticky="ew")

ttk.Label(selectors_frame, text="Диаметр печи, мм").grid(row=0, column=3, sticky="w")
furnace_D = ttk.Entry(selectors_frame)
furnace_D.grid(row=1, column=3, padx=(0, 15), sticky="ew")

ttk.Label(selectors_frame, text="Длинна печи, пог. м").grid(row=0, column=4, sticky="w")
furnace_L = ttk.Entry(selectors_frame)
furnace_L.grid(row=1, column=4, sticky="ew")

selectors_frame.columnconfigure(0, weight=1)
selectors_frame.columnconfigure(1, weight=1)
selectors_frame.columnconfigure(2, weight=1)
selectors_frame.columnconfigure(3, weight=1)
selectors_frame.columnconfigure(4, weight=1)

calculate_button = ttk.Button(main_frame, text="Рассчитать", command=submit)
calculate_button.pack(pady=20)

ttk.Label(main_frame, text="Результат").pack(anchor="w")

result_text = tk.Text(main_frame, height=12, wrap="word", state="disabled")
result_text.pack(fill=tk.BOTH, expand=True)

update_formats()

root.mainloop()