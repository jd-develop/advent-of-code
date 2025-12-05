

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


let parse_input (input: string list) : (int * int) list * int list =
  let rec parse_ranges (input: string list) (accu: (int * int) list) :
      (int * int) list * string list =
    match input with
    | [] -> failwith "Erreur de lecture : fin du fichier atteinte"
    | ""::q -> accu, q
    | s::q ->
        begin
        let a, b = match (String.split_on_char '-' s) with
        | [a; b] -> int_of_string a, int_of_string b
        | _ -> failwith "Erreur de lecture : range attendue" in
        parse_ranges q ((a, b)::accu)
        end
  in
  let ranges, ids = parse_ranges input [] in
  ranges, (List.filter_map int_of_string_opt ids)


let is_in_range ((a, b): int * int) (id: int) =
  a <= id && id <= b

let solve_part1 (ranges: (int * int) list) (ids: int list) : int =
  List.fold_left (
    fun sum id ->
      if (List.fold_left (
        fun acc range -> acc || (is_in_range range id)) false ranges
      )
      then sum+1
      else sum
  ) 0 ids


(* Zut, c’est pas récursif terminal *)
let rec insert_range (range_list: (int * int) list) ((a, b) : int * int) :
   (int * int) list =
  match range_list with
  | [] -> [(a, b)]
  | (a', b')::q ->
      if a' <= a && b <= b' then range_list
      else if a' <= a && a <= b' && b' <= b then (a', b)::q
      else if a <= a' && a' <= b && b <= b' then (a, b')::q
      else if a <= a' && b' <= b then (a, b)::q
      else (a', b')::(insert_range q (a, b))


let rec flatten_ranges (ranges: (int * int) list) =
  let new_ranges = ranges |>
    List.fold_left (fun l (a, b) -> insert_range l (a, b)) [] in
  if new_ranges = ranges then new_ranges
  else flatten_ranges new_ranges


let solve_part2 (ranges: (int * int) list) : int =
  ranges |> flatten_ranges
         |> List.fold_left (fun sum (a, b) -> sum + b-a+1) 0


let solve (filename: string) =
  let ranges, ids = parse_input (open_input (Some filename)) in
  print_int (solve_part1 ranges ids);
  print_newline ();
  print_int (solve_part2 ranges);
  print_newline ()
