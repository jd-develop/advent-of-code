
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


type problem =
  | Plus of int list
  | Times of int list


(* Splitte s sur les espaces (n’importe quel nombre) puis applique f aux
 * résultats (genre split_filter_empty_f f "a  b" = [f "a"; f "b"]) *)
let split_filter_empty_f (f: string -> 'a) (s: string) : 'a list =
  String.split_on_char ' ' s
  |> List.filter_map
    (fun s -> if s = "" then None else Some(f s))

let rec transpose (l: 'a list list) : 'a list list =
  match l with
  | [] -> []
  (* je sais pas si ce cas de base est bon, mais en vrai ça n’arrive pas donc
   * osef *)
  | []::q -> transpose q
  | l'::q ->
      let trans_q = transpose q in
      if trans_q = [] then List.map (fun x -> [x]) l' else
      List.map2 List.cons l' trans_q

let parse_for_part_1 (input: string list) : problem list =
  (* Il suffit de parse le tableau d’entrées puis de transposer, en faisant
   * attention aux + et aux * *)
  let rec to_int_list_list_and_op_list (l: string list) (accu: int list list) :
      (int list list * char list) =
    match l with
    | [] | [_] -> failwith "pas d’opérateurs"
    | [x; _] ->
        accu, split_filter_empty_f (fun s -> s.[0]) x
    | x::q -> to_int_list_list_and_op_list q
              ((split_filter_empty_f int_of_string x)::accu)
  in
  let numbers, operators = to_int_list_list_and_op_list input [] in
  let num_trans = transpose numbers in
  List.map2 (
    fun op l -> if op = '+' then Plus l else Times l
  ) operators num_trans

let parse_for_part_2 (input: string list) : problem list =
  (* Parse un problème et renvoie la liste des autres problèmes pas encore
   * parsés *)
  let rec one_problem (exp: char list list) : problem * char list list =
    let rec aux (l: char list list) (cur: int list) :
        int list * char list list =
      match l with
      | [] -> cur, l
      | []::q -> cur, q
      | (c::_)::l' when c = '+' || c = '*' -> cur, l'
      | (num)::l' ->
          let new_num =
            num
            |> List.filter_map (fun x -> if x = ' ' then None else Some x)
            |> List.rev
            |> List.to_seq
            |> String.of_seq
            |> int_of_string_opt
          in
          match new_num with
          | None -> cur, l'
          | Some new_num ->
            aux l' (new_num::cur)
    in
    match exp with
    | []::_
    | [] -> failwith "pas de problème à parse"
    | (c::p)::q ->
        if c = ' ' then
          one_problem q
        else
          let pb, next = aux (p::q) [] in
          if c = '+' then Plus(pb), next
          else Times(pb), next
  in
  let rec problems (exp: char list list) (accu: problem list) : problem list =
    match exp with
    | [] -> accu
    | _ -> let pb, next = one_problem exp in problems next (pb::accu)
  in
  let exploded =
    List.map (fun x -> List.of_seq (String.to_seq x)) input
    |> transpose
    |> List.(map rev)
  in
  problems exploded []


let solve_problems (input: problem list) =
  let rec aux (l: problem list) (sum: int) : int =
    match l with
    | [] -> sum
    | Plus(l)::q -> aux q (sum + List.fold_left (+) 0 l)
    | Times(l)::q -> aux q (sum + List.fold_left ( * ) 1 l)
  in
  aux input 0


let solve (f: string) =
  let input = open_input (Some f) in
  let problems1 = parse_for_part_1 input in
  print_int (solve_problems problems1);
  print_newline ();
  let problems2 = parse_for_part_2 input in
  print_int (solve_problems problems2);
  print_newline ();
