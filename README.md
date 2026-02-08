# 🧠 Apriori Algorithm GUI

A Python-based graphical user interface (GUI) for **association rule mining** using the **Apriori algorithm**.  
This tool allows users to easily upload Excel transaction data, set minimum support and confidence thresholds, and visualize frequent itemsets and strong association rules interactively.

---

## 🚀 Features

- 📂 **Excel File Input** — Load `.xlsx` files directly into the application.  
- ⚙️ **Custom Parameters** — Set minimum support and confidence values (in %).  
- 📊 **Visualization** — View bar charts of frequent itemsets and their support counts.  
- 🔍 **Association Rule Mining** — Generate strong rules based on the Apriori algorithm.  
- 📈 **Lift and Confidence Display** — Automatically compute lift and confidence for each rule.  
- 🖥️ **Dark Modern GUI** — Built using `tkinter` with `matplotlib` integration.

---

## 🧩 How It Works

1. **Load an Excel File**
   - The Excel file must have **at least two columns**.
   - The **second column** should contain transaction data,  
     where each transaction is a comma-separated list of items.
     ```
     Example:
     TiD | items
     1   | M,O,N,K,E,Y
     2   | D,O,N,K,E,Y
     3   | M,A,K,E
     ```

2. **Set Parameters**
   - Minimum Support (%)  
   - Minimum Confidence (%)

3. **Run Apriori**
   - Click **Run Apriori** to process your data.  
   - The GUI will display:
     - Frequent itemsets and their support counts
     - Strong association rules
     - Confidence and Lift values
     - Bar chart of frequent itemsets

---

## 🛠️ Requirements

Ensure you have **Python 3.8+** and the following libraries installed:

```bash
pip install pandas matplotlib openpyxl
```

---

## 🧾 Usage

### Run the application:
```bash
python apriori_gui.py
```

### Steps:
1. Click **“Browse Excel File”** to select your dataset (`.xlsx` file).  
2. Enter your **Minimum Support (%)** and **Minimum Confidence (%)** values.  
3. Click **“Run Apriori”** to execute the algorithm.  
4. View:
   - Frequent itemsets (with support counts)
   - Strong rules (with confidence and lift)
   - Visualized bar chart of supports

---

## 📊 Example Output

**Frequent Itemsets Table:**

| Type              | Itemset/Rule | Count/Confidence | Lift  |
|-------------------|--------------|------------------|-------|
| Frequent Itemset  | M,O          | 3                | —     |
| Association Rule  | ['M'] → ['O']| 0.8              | 1.25  |

**Bar Chart:**
Displays each frequent itemset’s support count as a colored bar.

---

## 🧮 Algorithm Overview

The **Apriori algorithm** identifies frequent itemsets in a dataset based on a minimum support threshold, then derives strong association rules that satisfy a minimum confidence threshold.

- **Support** = Frequency of an itemset  
- **Confidence** = `Support(X ∪ Y) / Support(X)`  
- **Lift** = `(Support(X ∪ Y) * N) / (Support(X) * Support(Y))`

---

## 📦 File Structure

```
📁 Apriori-GUI
│
├── apriori_gui.py      # Main Python script with GUI and algorithm
├── README.md           # Project documentation
└── sample_data.xlsx    # Example transaction dataset (optional)
```

---

## 🎨 GUI Preview

**Main Interface:**
- Dark theme
- Fields for parameters
- Buttons for file selection and running Apriori
- Interactive chart and results table

---

## 💡 Notes

- The **Excel file must contain transactions in the second column**.  
- The code uses `pandas.read_excel()` — ensure the file has a valid `.xlsx` format.  
- Results may vary based on the dataset size and parameter settings.  

---

## 🧑‍💻 Author

**Peter Refaat**  
💬 Developed in Python to simplify association rule mining visualization.

---

## 📜 License

This project is licensed under the **MIT License** — feel free to use, modify, and share.
