
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

let explode (s: string) : char list =
  s |> String.to_seq |> List.of_seq


(* Parses the input into a list of list of splitters (each line is represented
 * by the coordinates of its splitters). Also returns the index of the source on
 * the first line. *)
let parse_input (input: string list) : int list list * int =
  let rec splitters_coordinates (line: char list) (i: int)
      (accu: int list) : int list =
    match line with
    | [] -> List.rev accu
    | x::q -> if x = '^' then splitters_coordinates q (i+1) (i::accu)
              else splitters_coordinates q (i+1) accu
  in
  let rec parse_accu (remaining_lines: string list) (accu: int list list) :
      int list list =
    match remaining_lines with
    | [] | [_] -> List.rev accu
    | x::q -> parse_accu q ((splitters_coordinates (explode x) 0 [])::accu)
  in
  parse_accu input [], (String.length (List.hd input) / 2)


let rec enlever_doublons_rev (l: ('a * int) list) (accu: ('a * int) list) :
    ('a * int) list =
  match l with
  | [] -> accu
  | [x] -> x::accu
  | (x, mx)::(y, my)::q ->
      if x = y then
        enlever_doublons_rev ((x, mx+my)::q) accu
      else
        enlever_doublons_rev ((y, my)::q) ((x, mx)::accu)

let rec compter_avec_multiplicite (l: ('a * int) list) (accu: int) : int =
  match l with
  | [] -> accu
  | (_, i)::q -> compter_avec_multiplicite q (accu+i)


(* Tant qu’à faire, j’ai réutilisé la même fonction pour la partie 2.
 * L’idée est de compter les rayons avec multiplicité *)
let solve_both_parts (input: int list list) (source: int) (part2: bool) : int =
  let rec new_beams (line: int list) (beams: (int * int) list)
      (accu_beams: (int * int) list) (accu: int) : (int * int) list * int =
    match beams with
    | [] -> enlever_doublons_rev accu_beams [], accu
    | (b, mult)::q ->
        if List.mem b line then
          new_beams line q (((b-1), mult)::((b+1), mult)::accu_beams) (accu+1)
        else
          new_beams line q ((b, mult)::accu_beams) accu
  in
  (* on suppose `beams` triée dans l’ordre croissant *)
  let rec solve_accu (remaining_lines: int list list) (beams: (int * int) list)
      (accu: int) : int =
    match remaining_lines with
    | [] -> if part2 then compter_avec_multiplicite beams 0 else accu
    | x::q ->
        let beams', to_add = new_beams x beams [] 0 in
        solve_accu q beams' (accu+to_add)
  in
  solve_accu input [source, 1] 0


let solve (f: string) =
  let parsed, source = parse_input (open_input (Some f)) in
  print_int (solve_both_parts parsed source false);
  print_newline ();
  print_int (solve_both_parts parsed source true);
  print_newline ()
