import tkinter as tk
from os import stat_result
from tkinter import ttk
from standards.gost import gost
from standards.iso import iso
from standards.vdz import vdz


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
    except ValueError:
        raise Exception("Введи корректный диаметр")

    try:
        l = float(L)
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

    data = STANDARDS[selected_standard]

    brick_1 = data[format_1_name] if format_1_name in data else data[int(format_1_name)]
    brick_2 = data[format_2_name] if format_2_name in data else data[int(format_2_name)]
    d_outer = int(D_outer_raw)
    l = float(L_raw)

    render_result(f"Стандарт: {selected_standard}\n"
        f"Формат 1: {format_1_name} → {brick_1}\n"
        f"Формат 2: {format_2_name} → {brick_2}\n"
        f"Внутренний диаметр печи: {d_outer} мм\n"
        f"Длинна печи: {l} пог.м \n"
    )

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