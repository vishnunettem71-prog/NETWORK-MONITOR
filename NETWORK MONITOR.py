import tkinter as tk
from tkinter import ttk, messagebox
import psutil
import socket
import time
import threading
from datetime import datetime


class NetworkMonitor:
    def __init__(self, root):
        self.root = root
        self.root.title("Network Monitoring System")
        self.root.geometry("1000x650")
        self.root.configure(bg="#101820")

        self.running = True
        self.last_sent = psutil.net_io_counters().bytes_sent
        self.last_recv = psutil.net_io_counters().bytes_recv
        self.last_time = time.time()

        self.create_ui()
        self.update_monitor()

    def create_ui(self):

        # Title
        title = tk.Label(
            self.root,
            text="NETWORK MONITORING SYSTEM",
            font=("Arial", 24, "bold"),
            fg="#00e5ff",
            bg="#101820"
        )
        title.pack(pady=15)

        # System information frame
        info_frame = tk.Frame(self.root, bg="#18232c")
        info_frame.pack(fill="x", padx=20, pady=10)

        self.ip_label = self.create_info_label(
            info_frame, "IP Address", 0, 0
        )
        self.hostname_label = self.create_info_label(
            info_frame, "Hostname", 0, 1
        )
        self.time_label = self.create_info_label(
            info_frame, "Time", 0, 2
        )

        # Monitoring frame
        monitor_frame = tk.Frame(self.root, bg="#101820")
        monitor_frame.pack(fill="x", padx=20, pady=10)

        self.cpu_label = self.create_card(
            monitor_frame, "CPU Usage", 0
        )
        self.ram_label = self.create_card(
            monitor_frame, "RAM Usage", 1
        )
        self.disk_label = self.create_card(
            monitor_frame, "Disk Usage", 2
        )
        self.connections_label = self.create_card(
            monitor_frame, "Connections", 3
        )

        # Network traffic
        traffic_frame = tk.LabelFrame(
            self.root,
            text=" Network Traffic ",
            font=("Arial", 14, "bold"),
            fg="#00e5ff",
            bg="#18232c",
            padx=20,
            pady=15
        )
        traffic_frame.pack(fill="x", padx=20, pady=10)

        self.download_label = tk.Label(
            traffic_frame,
            text="Download Speed: 0 KB/s",
            font=("Arial", 16, "bold"),
            fg="#00ff88",
            bg="#18232c"
        )
        self.download_label.pack(pady=5)

        self.upload_label = tk.Label(
            traffic_frame,
            text="Upload Speed: 0 KB/s",
            font=("Arial", 16, "bold"),
            fg="#ffaa00",
            bg="#18232c"
        )
        self.upload_label.pack(pady=5)

        # Connection table
        table_frame = tk.LabelFrame(
            self.root,
            text=" Active Network Connections ",
            font=("Arial", 14, "bold"),
            fg="#00e5ff",
            bg="#18232c"
        )
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)

        columns = ("Local Address", "Remote Address", "Status", "PID")

        self.table = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings"
        )

        for column in columns:
            self.table.heading(column, text=column)
            self.table.column(column, width=200)

        self.table.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        # Refresh button
        self.refresh_button = tk.Button(
            self.root,
            text="REFRESH",
            font=("Arial", 12, "bold"),
            bg="#00e5ff",
            fg="black",
            command=self.update_monitor
        )
        self.refresh_button.pack(pady=10)

    def create_info_label(self, parent, title, row, column):

        frame = tk.Frame(
            parent,
            bg="#18232c",
            width=300,
            height=70
        )
        frame.grid(
            row=row,
            column=column,
            padx=20,
            pady=10
        )

        label = tk.Label(
            frame,
            text=title + "\nLoading...",
            font=("Arial", 12, "bold"),
            fg="white",
            bg="#18232c"
        )
        label.pack(padx=20, pady=10)

        return label

    def create_card(self, parent, title, column):

        frame = tk.Frame(
            parent,
            bg="#18232c",
            width=200,
            height=100
        )

        frame.grid(
            row=0,
            column=column,
            padx=10,
            pady=10
        )

        label = tk.Label(
            frame,
            text=title + "\n0%",
            font=("Arial", 15, "bold"),
            fg="#00e5ff",
            bg="#18232c"
        )

        label.pack(
            padx=30,
            pady=25
        )

        return label

    def update_monitor(self):

        try:
            # CPU
            cpu = psutil.cpu_percent(interval=0.1)

            # RAM
            ram = psutil.virtual_memory().percent

            # Disk
            disk = psutil.disk_usage("/").percent

            # Network connections
            try:
                connections = len(psutil.net_connections())
            except:
                connections = 0

            # IP Address
            hostname = socket.gethostname()

            try:
                ip = socket.gethostbyname(hostname)
            except:
                ip = "Unavailable"

            # Current time
            current_time = datetime.now().strftime(
                "%d-%m-%Y %H:%M:%S"
            )

            # Network speed
            net = psutil.net_io_counters()

            current_time_seconds = time.time()

            time_difference = (
                current_time_seconds - self.last_time
            )

            if time_difference > 0:

                upload_speed = (
                    net.bytes_sent - self.last_sent
                ) / time_difference

                download_speed = (
                    net.bytes_recv - self.last_recv
                ) / time_difference

            else:
                upload_speed = 0
                download_speed = 0

            self.last_sent = net.bytes_sent
            self.last_recv = net.bytes_recv
            self.last_time = current_time_seconds

            # Update labels
            self.cpu_label.config(
                text=f"CPU Usage\n{cpu}%"
            )

            self.ram_label.config(
                text=f"RAM Usage\n{ram}%"
            )

            self.disk_label.config(
                text=f"Disk Usage\n{disk}%"
            )

            self.connections_label.config(
                text=f"Connections\n{connections}"
            )

            self.ip_label.config(
                text=f"IP Address\n{ip}"
            )

            self.hostname_label.config(
                text=f"Hostname\n{hostname}"
            )

            self.time_label.config(
                text=f"Time\n{current_time}"
            )

            self.download_label.config(
                text=f"Download Speed: "
                     f"{download_speed / 1024:.2f} KB/s"
            )

            self.upload_label.config(
                text=f"Upload Speed: "
                     f"{upload_speed / 1024:.2f} KB/s"
            )

            # Update connections table
            for item in self.table.get_children():
                self.table.delete(item)

            try:
                connections_list = psutil.net_connections(
                    kind="inet"
                )

                for conn in connections_list[:50]:

                    local_address = ""

                    if conn.laddr:
                        local_address = (
                            f"{conn.laddr.ip}:"
                            f"{conn.laddr.port}"
                        )

                    remote_address = ""

                    if conn.raddr:
                        remote_address = (
                            f"{conn.raddr.ip}:"
                            f"{conn.raddr.port}"
                        )

                    status = conn.status
                    pid = conn.pid if conn.pid else "-"

                    self.table.insert(
                        "",
                        "end",
                        values=(
                            local_address,
                            remote_address,
                            status,
                            pid
                        )
                    )

            except Exception:
                pass

            # Automatically refresh every 2 seconds
            if self.running:
                self.root.after(
                    2000,
                    self.update_monitor
                )

        except Exception as e:
            print("Error:", e)

    def close_application(self):
        self.running = False
        self.root.destroy()


# Main program
if __name__ == "__main__":

    try:
        import psutil
    except ImportError:

        print(
            "psutil is not installed.\n"
            "Run: pip install psutil"
        )

        messagebox.showerror(
            "Missing Library",
            "Please install psutil using:\n\n"
            "pip install psutil"
        )

        exit()

    root = tk.Tk()

    app = NetworkMonitor(root)

    root.protocol(
        "WM_DELETE_WINDOW",
        app.close_application
    )

    root.mainloop()