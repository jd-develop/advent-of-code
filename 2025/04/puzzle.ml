

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


let parse_input (input: string list) : bool list list =
  List.filter_map (
    fun s ->
      if s = "" then None
      else Some (List.map (
        fun c -> c = '@'
      ) (List.of_seq (String.to_seq s)))
  ) input


let number_of_true (l: bool list) : int =
  List.fold_left (fun sum b -> if b then sum+1 else sum) 0 l


(* I KNOW there are so-called “easier” solutions with what inferior beings
 * call “imperative programming”, but we don’t do that here. *)
let rec count
    (previous_line: bool list)
    (current_line: bool list)
    (next_line: bool list)
    (lines_including_the_current: bool list list)
    (counter: int)
    (previous_on_current_line: bool)
    (previous_on_previous_line: bool)
    (previous_on_next_line: bool)
    (line_length: int)
    (current_index: int * int)
    (can_be_removed : (int * int) list) : int * (int * int) list =
  match current_line with
  | [] -> begin
    match lines_including_the_current with
    | [] | [_] | [_; _] -> counter, can_be_removed
    | current::next::next_next::q ->
        count current next next_next (next::next_next::q) counter false false
              false line_length (fst current_index + 1, 0) can_be_removed
    end
  | [x] -> begin
    match previous_line, next_line with
    | [x1], [x2] ->
        let new_counter, new_can_be_removed =
          if not x then counter, can_be_removed else
            let voisins = number_of_true [
              previous_on_current_line; previous_on_next_line;
              previous_on_previous_line; x1; x2
            ] in
            if voisins < 4 then
              counter + 1, (current_index::can_be_removed)
            else
              counter, can_be_removed in
        count [] [] [] lines_including_the_current new_counter x x1 x2
              line_length (fst current_index, snd current_index + 1)
              new_can_be_removed
    | _ -> failwith "non1"
    end
  | x::y::q -> begin
    match previous_line, next_line with
    | x1::y1::q1, x2::y2::q2 ->
        let new_counter, new_can_be_removed =
          if not x then counter, can_be_removed else
            let voisins = number_of_true [
              previous_on_previous_line; previous_on_next_line;
              previous_on_current_line;
              x1; x2; y; y1; y2
            ] in
            if voisins < 4 then
              counter + 1, (current_index::can_be_removed)
            else
              counter, can_be_removed in
        count (y1::q1) (y::q) (y2::q2) lines_including_the_current new_counter
               x x1 x2 line_length (fst current_index, snd current_index + 1)
               new_can_be_removed
    | _ -> failwith "non2"
    end


let solve_part1 (input: bool list list) =
  match input with
  | [] | [_] -> 0
  | x::y::q ->
      let list_length = List.length x in
      let line_of_false = List.init list_length (fun _ -> false) in
      count line_of_false x y (input@[line_of_false]) 0 false false false
            list_length (0, 0) []
      |> fst


let rec remove_indexes (ll: bool list list) (current: bool list)
    (accu: bool list list) (current_accu: bool list) (current_idx: int * int)
    (should_remove: (int * int) list) : bool list list =
  match current with
  | [] ->
    let new_accu = current_accu::accu in
    begin match ll with
    | [] -> List.rev (List.map List.rev new_accu)
    | x::q -> remove_indexes q x new_accu [] (fst current_idx + 1, 0)
              should_remove
    end
  | x::q ->
      let new_current_accu =
        ((not (List.mem current_idx should_remove)) && x)::current_accu in
      remove_indexes ll q accu new_current_accu
      (fst current_idx, snd current_idx + 1) should_remove


let solve_part2 (input: bool list list): int =
  let rec solve_acc (sum: int) (current: bool list list) =
    match current with
    | [] | [_] -> 0
    | x::y::q ->
      let list_length = List.length x in
      let line_of_false = List.init list_length (fun _ -> false) in
      let res, should_remove = count line_of_false x y (current@[line_of_false])
                               0 false false false list_length (0, 0) [] in
      begin match should_remove with
      | [] -> res+sum
      | _ ->
          let next = remove_indexes (y::q) x [] [] (0, 0) should_remove in
          solve_acc (res+sum) next
      end
  in
  solve_acc 0 input


let solve (filename: string) =
  let input = parse_input (open_input (Some filename)) in
  print_int (solve_part1 input);
  print_newline ();
  print_int (solve_part2 input);
  print_newline ()
