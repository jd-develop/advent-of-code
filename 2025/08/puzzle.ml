
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


let parse_input (input: string list) : (int * int * int) list =
  List.filter_map (
    fun s ->
      if s = "" then
        None
      else
        match List.map int_of_string (String.split_on_char ',' s) with
        | [a; b; c] -> Some(a, b, c)
        | _ -> None
  ) input


type point = int * int * int
type two_points = point * point

let sq a = a*a
(* because sqrt is increasing, we can get rid of it and only use integers *)
let distance (x1, y1, z1: point) (x2, y2, z2: point) : int =
  sq (x2-x1) + sq (y2-y1) + sq (z2-z1)


let rec points_in_connected_component (s: point) (vertices: two_points list)
    (visited: point list) : int * point list =
  if List.mem s visited then 0, visited
  else
    let voisins =
      List.filter_map
      (fun (a, b) -> if a = s then Some b else if b = s then Some a else None)
      vertices
    in
    List.fold_left
    (fun (acc, v) p ->
      let sum, new_v = points_in_connected_component p vertices v in
      acc+sum, new_v)
    (1, s::visited) voisins


let rec connected_components (data: point list) (visited: point list)
    (accu: int list) (vertices: two_points list) : int list =
  match data with
  | [] -> List.sort compare accu |> List.rev
  | x::q ->
      if List.mem x visited then
        connected_components q visited accu vertices
      else
        let sum, new_v = points_in_connected_component x vertices visited in
        connected_components q new_v (sum::accu) vertices


(* cartesian product *)
(* not tail-recursive… *)
let rec ( ** ) (l: 'a list) (l': 'b list) : ('a * 'b) list =
  match l with
  | [] -> []
  | x::q -> (List.map (fun a -> (x, a)) l')@(q ** l')

let rec first_n (n: int) (accu: 'a list) (l: 'a list) : 'a list =
  if n = 0 then
    List.rev accu
  else
    List.(first_n (n-1) (hd l::accu) (tl l))

(* called in solve *)
let sorted_by_distance_descending (data: point list) : two_points list =
  data ** data
  |> List.filter_map
    (fun (a, b) -> if a >= b then None else Some(a, b, distance a b))
  |> List.sort (fun (_, _, a) (_, _, b) -> a-b)
  |> List.map (fun (a, b, _) -> (a, b))

let solve_part_1 (data: point list) (sorted: two_points list)
    (how_many: int) : int =
  sorted
  |> first_n how_many []
  |> connected_components data [] []
  |> first_n 3 []
  |> List.fold_left ( * ) 1


(* hmmmmm *)
type number =
  | Zero
  | One
  | Many

let rec how_many_connected_components (data: point list) (visited: point list)
    (vertices: two_points list) (seen_one: bool) : number =
  match data with
  | [] -> if seen_one then One else Zero
  | x::q ->
      if List.mem x visited then
        how_many_connected_components q visited vertices seen_one
      else
        if seen_one then Many
        else
          let new_v = snd (points_in_connected_component x vertices visited) in
          how_many_connected_components q new_v vertices true

(* This function takes forever, so I ran it during dinner :)
 * Ironically, I don’t have time to optimise it *)
let rec solve_part_2 (data: point list) (sorted: two_points list)
    (vertices : two_points list) : int =
  match sorted with
  | [] -> failwith "pas de donnée"
  | (a, b)::q ->
      match how_many_connected_components data [] ((a, b)::vertices) false with
      | One -> let x1, _, _ = a in let x2, _, _ = b in x1*x2
      | _ -> solve_part_2 data q ((a, b)::vertices)

let solve (f: string) (n: int) =
  let data = parse_input (open_input (Some f)) in
  let sorted = sorted_by_distance_descending data in
  print_int (solve_part_1 data sorted n);
  print_newline ();
  print_int (solve_part_2 data (List.tl sorted) [List.hd sorted]);
  print_newline ()
