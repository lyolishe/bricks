import tkinter as tk
from tkinter import ttk
from standards.gost import gost
from standards.iso import iso
from standards.vdz import vdz


STANDARDS = {
    "ГОСТ": gost,
    "ISO": iso,
    "VDZ": vdz,
}


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


def calculate():
    selected_standard = standard_select.get()
    format_1 = first_format.get()
    format_2 = second_format.get()

    data = STANDARDS[selected_standard]

    brick_1 = data[format_1] if format_1 in data else data[int(format_1)]
    brick_2 = data[format_2] if format_2 in data else data[int(format_2)]

    result_text.delete("1.0", tk.END)
    result_text.insert(
        tk.END,
        f"Стандарт: {selected_standard}\n"
        f"Формат 1: {format_1} → {brick_1}\n"
        f"Формат 2: {format_2} → {brick_2}\n"
    )


root = tk.Tk()
root.title("Расчёт футеровки клиновым кирпичем")
root.geometry("700x450")


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
second_format.grid(row=1, column=2, sticky="ew")

selectors_frame.columnconfigure(0, weight=1)
selectors_frame.columnconfigure(1, weight=1)
selectors_frame.columnconfigure(2, weight=1)

calculate_button = ttk.Button(main_frame, text="Рассчитать", command=calculate)
calculate_button.pack(pady=20)

ttk.Label(main_frame, text="Результат").pack(anchor="w")

result_text = tk.Text(main_frame, height=12, wrap="word")
result_text.pack(fill=tk.BOTH, expand=True)

update_formats()

root.mainloop()