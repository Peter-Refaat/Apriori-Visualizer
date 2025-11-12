from collections import defaultdict
from pandas import read_excel
import math
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from matplotlib import cm


def run_apriori(file_path, min_support_percent, min_confidence_percent):
    dt = read_excel(file_path)

    min_support = min_support_percent / 100
    min_confidence = min_confidence_percent / 100
    min_support_count = math.ceil(min_support * len(dt))

    unique_items = set()
    for transaction in dt.iloc[:, 1]:
        items = transaction.split(',')
        for item in items:
            unique_items.add(item)

    strong_association_rules = []
    confidence = defaultdict(float)

    itemset_support_count = defaultdict(int)
    for transaction in dt.iloc[:, 1]:
        items = transaction.split(',')
        cur_dict = defaultdict(int)
        for item in items:
            cur_dict[item] = 1
        for item in cur_dict:
            itemset_support_count[tuple(item)] += 1

    def is_frequent(check_itemset):
        cnt = 0
        for itemset in dt.iloc[:, 1]:
            items = itemset.split(',')
            can = True
            for item in check_itemset:
                if item not in items:
                    can = False
                    break
            cnt += can
        return (cnt >= min_support_count,cnt)

    def apriori():
        frequent_itemsets = defaultdict(list)
        cur = []
        for item, count in itemset_support_count.items():
            if count >= min_support_count:
                cur.append(list(item))
        cur.sort()
        lvl = 1
        while len(cur) > 1:
            nxt_cur = []
            for itemset in cur:
                frequent_itemsets[lvl].append(itemset)
            for i in range(len(cur)):
                for j in range(i + 1 , len(cur)):
                    cnt = 0
                    for k in range(lvl):
                        if cur[i][k] != cur[j][k]:
                            break
                        cnt += 1
                    if lvl == 1:
                        nxt = [cur[i][0] , cur[j][0]]
                        frequent, sup_count = is_frequent(nxt)
                        if frequent:
                            nxt_cur.append(nxt)
                            itemset_support_count[tuple(nxt)] = sup_count
                    elif cnt == lvl - 1:
                        nxt = cur[i] + [cur[j][-1]]
                        frequent, sup_count = is_frequent(nxt)
                        if frequent:
                            nxt_cur.append(nxt)
                            itemset_support_count[tuple(nxt)] = sup_count
                    else:
                        break
            cur = nxt_cur
            lvl += 1
        frequent, sup_count = is_frequent(cur[0])
        if(frequent):
            itemset_support_count[tuple(cur[0])] = sup_count
            frequent_itemsets[lvl].append(cur[0])
        return frequent_itemsets

    def get_confidence(before,after):
        before_frequent, before_count = is_frequent(before)
        combined = before + after
        combined_frequent, combined_count = is_frequent(combined)
        return combined_count / before_count

    def generate_association_rules(itemset):
        n = len(itemset)
        for msk in range(0,1 << n):
            if bin(msk).count('1') == 0 or bin(msk).count('1') == n:
                continue
            before = []
            after = []
            for i in range(len(itemset)):
                if (msk >> i) & 1:
                    before.append(itemset[i])
                else:
                    after.append(itemset[i])
            cur_confidence = get_confidence(list(before), list(after))
            if cur_confidence >= min_confidence:
                strong_association_rules.append(str(before) + " -> " + str(after))
                confidence[str(before) + " -> " + str(after)] = cur_confidence

    frequent_itemsets = apriori()
    for lvl, itemsets in frequent_itemsets.items():
        for itemset in itemsets:
            generate_association_rules(itemset)

    lift = {}
    for rule in strong_association_rules:
        before_str, after_str = rule.split(" -> ")
        before = eval(before_str)
        after = eval(after_str)
        combined = before + after
        before_frequent, before_count = is_frequent(before)
        after_frequent, after_count = is_frequent(after)
        combined_frequent, combined_count = is_frequent(combined)
        lift_val = (combined_count * len(dt)) / (before_count * after_count) if before_count * after_count > 0 else 0
        lift[rule] = lift_val

    return frequent_itemsets, itemset_support_count, strong_association_rules, confidence, lift

class AprioriGUI:
    def __init__(self, root):
        self.root = root
        root.title("Apriori Algorithm GUI")
        root.geometry("1100x700")
        root.configure(bg="#2e2e2e")

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background="#3c3f41", foreground="white", fieldbackground="#3c3f41", rowheight=25)
        style.configure("Treeview.Heading", background="#45494a", foreground="white")
        style.map('Treeview', background=[('selected', '#6a9fb5')])

        self.input_frame = tk.Frame(root, bg="#2e2e2e", padx=10, pady=10)
        self.input_frame.pack(fill="x")

        tk.Label(self.input_frame, text="Minimum Support (%)", fg="white", bg="#2e2e2e").grid(row=0, column=0, sticky="w")
        self.support_entry = tk.Entry(self.input_frame, width=10, bg="#45494a", fg="white")
        self.support_entry.grid(row=0, column=1)
        self.support_entry.insert(0, "60")

        tk.Label(self.input_frame, text="Minimum Confidence (%)", fg="white", bg="#2e2e2e").grid(row=0, column=2, sticky="w", padx=(20,0))
        self.confidence_entry = tk.Entry(self.input_frame, width=10, bg="#45494a", fg="white")
        self.confidence_entry.grid(row=0, column=3)
        self.confidence_entry.insert(0, "80")

        tk.Button(self.input_frame, text="Browse Excel File", bg="#6a9fb5", fg="white", command=self.select_file).grid(row=0, column=4, padx=(20,0))
        tk.Button(self.input_frame, text="Run Apriori", bg="#6a9fb5", fg="white", command=self.run_apriori_gui).grid(row=0, column=5, padx=(20,0))

        self.chart_frame = tk.Frame(root, bg="#2e2e2e")
        self.chart_frame.pack(fill="both", expand=True, pady=(10,0))

        self.table_frame = tk.Frame(root, bg="#2e2e2e")
        self.table_frame.pack(fill="both", expand=True, pady=(10,0))

        self.table = ttk.Treeview(self.table_frame)
        self.table.pack(side="left", fill="both", expand=True)
        scrollbar = ttk.Scrollbar(self.table_frame, orient="vertical", command=self.table.yview)
        scrollbar.pack(side="right", fill="y")
        self.table.configure(yscroll=scrollbar.set)

    def select_file(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
        if self.file_path:
            messagebox.showinfo("Selected File", self.file_path)

    def run_apriori_gui(self):
        if not hasattr(self, "file_path") or not self.file_path:
            messagebox.showerror("Error", "Please select an Excel file first")
            return

        try:
            min_sup = float(self.support_entry.get())
            min_conf = float(self.confidence_entry.get())
        except:
            messagebox.showerror("Error", "Please enter valid numeric values")
            return

        frequent_itemsets, itemset_support_count, strong_rules, confidence_dict, lift_dict = run_apriori(self.file_path, min_sup, min_conf)

        for widget in self.chart_frame.winfo_children():
            widget.destroy()

        labels = []
        counts = []
        colors = []
        color_map = cm.get_cmap("tab20")
        idx = 0
        for lvl, itemsets in frequent_itemsets.items():
            for itemset in itemsets:
                labels.append(",".join(itemset))
                counts.append(itemset_support_count[tuple(itemset)])
                colors.append(color_map(idx % 20))
                idx += 1

        if labels:
            fig, ax = plt.subplots(figsize=(10, 4))
            ax.bar(labels, counts, color=colors)
            ax.set_xlabel("Frequent Itemsets", color="white")
            ax.set_ylabel("Support Count", color="white")
            ax.set_title("Frequent Itemsets", color="white")
            ax.tick_params(axis='x', rotation=45, colors='white')
            ax.tick_params(axis='y', colors='white')
            fig.patch.set_facecolor('#2e2e2e')
            ax.set_facecolor('#2e2e2e')
            plt.tight_layout()

            canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True)

        self.table.delete(*self.table.get_children())
        self.table["columns"] = ("Type", "Itemset/Rule", "Count/Confidence", "Lift")
        self.table.heading("#0", text="")
        self.table.column("#0", width=0, stretch=False)
        self.table.heading("Type", text="Type")
        self.table.heading("Itemset/Rule", text="Itemset/Rule")
        self.table.heading("Count/Confidence", text="Count/Confidence")
        self.table.heading("Lift", text="Lift")
        self.table.column("Itemset/Rule", width=400)

        for lvl, itemsets in frequent_itemsets.items():
            for itemset in itemsets:
                rule_str = ",".join(itemset)
                lift_val = lift_dict.get(rule_str, "")  # Lift for single itemsets may be empty
                self.table.insert("", "end", values=("Frequent Itemset", rule_str, itemset_support_count[tuple(itemset)], lift_val))

        for rule in strong_rules:
            lift_val = lift_dict.get(rule, "")
            self.table.insert("", "end", values=("Association Rule", rule, confidence_dict[rule], lift_val))

root = tk.Tk()
app = AprioriGUI(root)
root.mainloop()
