
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


(* Parses the input into a list of ranges *)
let parse_input (input: string list) : (int * int) list =
  let s = match input with
  | [] -> assert false;
  | x::_ -> x
  in
  let string_ranges1 = String.split_on_char ',' s in
  let string_ranges2 = List.map (fun x -> String.split_on_char '-' x) string_ranges1 in
  let int_ranges = List.map (fun l ->
    match l with
    | [a; b] -> int_of_string a, int_of_string b
    | _ -> assert false) string_ranges2 in
  int_ranges


let clean_range ((a, b): (int * int)) : (int * int) option =
  let b_power_of_10 = int_of_float (log10 (float_of_int b)) in
  let a_power_of_10 = int_of_float (log10 (float_of_int a)) in
  let new_b =
    if b_power_of_10 mod 2 = 1 then
      b
    else
      int_of_float (exp ((float_of_int b_power_of_10) *. (log 10.))) - 1
  in
  let new_a =
    if a_power_of_10 mod 2 = 1 then
      a
    else
      int_of_float (exp ((float_of_int (a_power_of_10 + 1)) *. (log 10.)))
  in
  if new_a >= new_b then
    None
  else
    Some(new_a, new_b)


let twice_the_number (num: int) : int =
  string_of_int num ^ string_of_int num |> int_of_string


let add_invalid_ids (acc: int) ((a, b): (int * int)) : int =
  let a_str = string_of_int a in
  let a_first_part = String.sub a_str 0 (String.length a_str / 2) in
  let a_first_part_int = int_of_string a_first_part in

  let rec test_from_to_b (start: int) (accu: int) : int =
    let current = twice_the_number start in
    if current > b then accu
    else if current < a then test_from_to_b (start+1) accu
    else test_from_to_b (start+1) (accu + current)
  in

  acc + (test_from_to_b a_first_part_int 0)


let solve_part1 (input: (int * int) list) =
  let cleaned_input = List.filter_map clean_range input in
  List.fold_left add_invalid_ids 0 cleaned_input


let rec number_repeted_n_times (num: int) (n: int) : int =
  if n = 1 then num
  else string_of_int num ^ string_of_int (number_repeted_n_times num (n-1))
        |> int_of_string


let add_invalid_ids_part2 (acc: int) ((a, b) : int * int) : int =
  let rec test_repeat_n (start: int) (accu: int) (n: int) (already_tested: int list) : int * int list =
    let current = number_repeted_n_times start n in
    if current > b then
      accu, already_tested
    else if current < a || List.mem current already_tested then
      test_repeat_n (start+1) accu n already_tested
    else
      test_repeat_n (start+1) (accu + current) n (current::already_tested)
  in

  let rec test_all_repeated_n_times (accu: int) (n: int)
      (already_tested: int list) =
    if number_repeted_n_times 1 n > b then
      accu
    else
      let to_add, new_tested = test_repeat_n 1 0 n already_tested in
      test_all_repeated_n_times (accu + to_add) (n+1) new_tested
  in

  acc + test_all_repeated_n_times 0 2 []


let solve_part2 (input: (int * int) list) =
  List.fold_left add_invalid_ids_part2 0 input


let solve (file: string) =
  let input = parse_input (open_input (Some file)) in
  print_int (solve_part1 input);
  print_newline ();
  print_int (solve_part2 input);
  print_newline ()
