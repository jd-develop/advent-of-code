
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


let explode s = s |> String.to_seq |> List.of_seq
let implode l = l |> List.to_seq |> String.of_seq


let (^) x n =
  let rec expo_rapide x n accu =
    if n = 0 then accu
    else if n mod 2 = 1 then
      expo_rapide (x*x) (n/2) (x*accu)
    else
      expo_rapide (x*x) (n/2) accu
  in expo_rapide x n 1


type machine = int * (int list) * (int list)


let parse_input (input: string list) : machine list =
  let rec bool_list_to_base_2 (l: bool list) : int =
    List.fold_left (fun a x -> a*2+(if x then 1 else 0)) 0 l
  in
  let rec parse_lights (machine: char list) (accu: bool list) :
      int * char list =
    match machine with
    | ']'::' '::q -> bool_list_to_base_2 accu, q
    | c::q -> parse_lights q ((c = '#')::accu)
    | _ -> failwith "non"
  in
  let rec parse_switch (machine: char list) (accu: int) :
      int * char list =
    match machine with
    | ' '::q -> accu, q
    | c::')'::q
    | c::','::q -> parse_switch q (accu + (2^(int_of_char c - 0x30)))
    | _ -> failwith "non 2"
  in
  let rec parse_switches (machine: char list) (accu: int list) :
      int list * char list =
    match machine with
    | '{'::q -> List.rev accu, machine
    | '('::q ->
        let switch, q' = parse_switch q 0 in
        parse_switches q' (switch::accu)
    | _ -> print_string (implode machine); failwith "non 3"
  in
  let parse_joltages (machine: char list) : int list =
    let nombres = String.sub (implode machine) 1 (List.length machine - 2) in
    List.map int_of_string (String.split_on_char ',' nombres)
  in
  let parse_machine (machine: char list) : machine =
    let light, reste = parse_lights (List.tl machine) [] in
    let switches, reste2 = parse_switches reste [] in
    let joltages = parse_joltages reste2 in
    light, switches, joltages
  in
  let rec parse_machines (input: string list) (accu: machine list) :
      machine list =
    match input with
    | [] | [""] -> List.rev accu
    | x::q -> parse_machines q ((x |> explode |> parse_machine)::accu)
  in
  parse_machines input []


let solve_machine (m: machine) : int =
  let rec aux (target: int) (current: int) (remaining_switches: int list)
              (n: int) : int option =
    match remaining_switches with
    | [] -> if current = target then (Some n) else None
    | x::q ->
        let choose_x = aux target (current lxor x) q (n+1) in
        let not_choose_x = aux target current q n in
        match choose_x, not_choose_x with
        | None, None -> None
        | Some a, None
        | None, Some a -> Some a
        | Some a, Some b -> Some (min a b)
  in
  let target, switches, _ = m in
  Option.get (aux target 0 switches 0)


let solve_part_1 (input: machine list) : int =
  List.fold_left (fun a m -> a+(solve_machine m)) 0 input


let rec (--) (l1: int list) (l2: int list) : int list =
  match (l1, l2) with
  | [], [] -> []
  | x::q, y::q' -> (x-y)::(q--q')
  | _ -> raise (Invalid_argument "listes de longueur différentes")


let ( ** ) a = List.map (fun x -> a*x)


(* transforme juste l’équation, ne la résoud pas tout de suite *)
(* AAAAAAAAAAARG cette fonction ne marche pas
 * contre-exemple :
 * pivot_gauss [[1; 1; 0],0;[1; 1; 1],1;[0;1;0],0] *)
let pivot_gauss (coeffs: (int list * int) list) : (int list * int) list =
  let rec aux (c: (int list * int) list) (accu: (int list * int) list) =
    match c with
    | [] -> accu (* je ne List.rev pas parce qu’on va regarder le pivot dans
                  * ce sens lors de la résolution *)
    | [x] -> aux [] (x::accu)
    | (x, ax)::(y, ay)::q ->
        begin match y with
        | [] -> accu
        | 0::qy ->
            let new_list =
              List.map (fun (l, a) -> (List.tl l, a)) ((y, ay)::q) in
            aux new_list ((x, ax)::accu)
        | n::qy ->
            let coeff_x = List.hd x in
            let new_y = (coeff_x ** y) -- (n ** x) in
            let new_ay = coeff_x*ay - n*ax in
            let new_list =
              List.map (fun (l, a) -> (List.tl l, a)) ((new_y, new_ay)::q) in
            aux (new_list) ((x, ax)::accu)
        end
  in
  (* on essaye d’avoir déjà un semblant de pivot *)
  aux (List.rev (List.sort compare coeffs)) []


let int_of_bool b = if b then 1 else 0


let pivot_de_gauss_of_machine (m: machine) : (int list * int) list =
  let _, switches, joltages = m in
  List.mapi
    (
      fun i x ->
        List.fold_right (
          fun switch acc ->
            let new_coeff = (switch lsr i) land 1 in
            new_coeff::acc
        ) switches [],
      x
    )
  joltages
  |> pivot_gauss


(* TODO *)
let solve_pivot_gauss (p: (int list * int) list) = 0

let solve_machine_part2 (m: machine) : int =
  m |> pivot_de_gauss_of_machine
    |> solve_pivot_gauss

let solve_part_2 : machine list -> int =
  List.fold_left (fun acc m -> acc+(solve_machine_part2 m)) 0


let solve (f: string) =
  let input = parse_input (open_input (Some f)) in
  print_int (solve_part_1 input);
  print_newline ();
  print_int (solve_part_2 input);
  print_newline ()
