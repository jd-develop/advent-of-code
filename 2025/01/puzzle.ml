
let open_input (input_f: string option) : string list =
  let real_name = match input_f with
  | Some s -> s
  | None -> "input"
  in
  let input_channel = open_in real_name in
  let input_contents =
    really_input_string input_channel (in_channel_length input_channel) in
  close_in input_channel;
  String.split_on_char '\n' input_contents


(* Parse input into a list of rotations. -1 = left, 1 = right. *)
let parse_input (input: string list) : (int * int) list =
  let parse_one_line (line: string) : (int * int) option =
    if line = "" then None else
    let left_or_right = if line.[0] = 'L' then (-1) else 1 in
    let number = int_of_string (String.sub line 1 (String.length line - 1)) in
    Some (left_or_right, number)
  in
  List.filter_map parse_one_line input


(* mathematical modulo *)
let (%) a b = (a mod b + b) mod b


(* Solve part 1 *)
let solve_part_1 (input: (int * int) list) : int =
  let next ((zeroes, current_num): int * int)
      ((plus_minus, how_much): (int * int)) : int * int =
    let new_num = (current_num + plus_minus * how_much) % 100 in
    if new_num = 0 then
      (zeroes+1, new_num)
    else
      (zeroes, new_num)
  in
  List.fold_left next (0, 50) input |> fst


(* Solve part 2 *)
let solve_part_2 (input: (int * int) list) : int =
  let next ((zeroes, current_num): int * int)
      ((plus_minus, how_much): (int * int)) : int * int =
    let new_num = current_num + plus_minus * how_much in
    let real_new_num = new_num % 100 in
    let clicks =
      if new_num <= 0 then
        if current_num = 0 then
          -(new_num/100)
        else
          1-(new_num/100)
      else new_num/100 in
    (zeroes+clicks, real_new_num)
  in
  List.fold_left next (0, 50) input |> fst


let solve (file: string) : unit =
  let input = open_input (Some file) in
  let parsed = parse_input input in
  print_int (solve_part_1 parsed);
  print_newline ();
  print_int (solve_part_2 parsed);
  print_newline ()
