
def save_solution_to_file(solution, fitness, file_path, time_elapsed):
    with open(file_path, "w") as file:
        file.write(f"NAME : {file_path.split('/')[-1]}\n")
        file.write("TYPE : TOUR\n")
        file.write(f"DIMENSION : {len(solution)}\n")
        file.write(f"COMMENT : Tour length: {round(fitness, 4)}\n")
        file.write(f"COMMENT : Time elapsed: {round(time_elapsed, 2)} [s]\n")
        file.write("TOUR_SECTION\n")
        for node in solution:
            file.write(f"{node}\n")
        file.write("-1\n")
        file.write("EOF\n")
