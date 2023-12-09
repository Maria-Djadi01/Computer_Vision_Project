
mean_vois = tk.Entry(right_frame, width=15)
mean_vois.grid(row=4, column=1, padx=10, pady=10)
mean_vois.insert(0, "Neighbors")  # Set a placeholder
mean_vois.config(fg="grey")  # Set the text color to grey

# Bind events to the entry to handle placeholder behavior
mean_vois.bind("<FocusIn>", lambda event, e=mean_vois: on_entry_click(e, "Neighbors"))
mean_vois.bind("<FocusOut>", lambda event, e=mean_vois: on_focus_out(e, "Neighbors"))

button4 = tk.Button(
    right_frame,
    text="Mean",
    width=15,
    command=lambda: apply_filter(
        np.array(image), mean_filter, vois=int(mean_vois.get())
    ),
).grid(row=4, column=0, padx=10, pady=10)