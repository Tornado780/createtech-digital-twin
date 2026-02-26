def optimize_schedule(model, rain, labor, material_delay, productivity):
    
    best_labor = labor + 15
    improved_productivity = productivity + 0.1
    
    optimized_delay = model.predict(
        [[rain, best_labor, material_delay, improved_productivity]]
    )[0]

    return max(optimized_delay, 0), best_labor, improved_productivity