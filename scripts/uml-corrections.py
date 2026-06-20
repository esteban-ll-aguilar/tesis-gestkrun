"""
Script de corrección del diagrama de clases UML (Draw.io JSON).

Aplica todas las correcciones identificadas en la auditoría:
1. Convierte Rol de clase a enumeración
2. Elimina validarLimiteWIP() de Usuario
3. Reduce TipoMensaje a solo PROYECTO y TAREA
4. Agrega Epica como entidad
5. Agrega TaskStateTransition como entidad
6. Agrega EstadoModulo como enumeración
7. Corrige relación Sprint → Módulo a Sprint → Proyecto
8. Agrega relación HistoriaUsuario → Módulo
9. Elimina PAUSADO de EstadoProyecto
10. Elimina limiteWIP de Proyecto

Uso: python scripts/uml-corrections.py
"""

import json
import os
import copy
from typing import Any

UML_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                        "docs", "uml", "Scrum-Diagrama de clases.json")


def load_json(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path: str, data: dict) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"Saved: {path}")


def find_cells(data: dict, label: str = None, cell_type: str = None) -> list:
    cells = data["pages"][0]["cells"]
    results = []
    for cell in cells:
        if label and cell.get("label") == label:
            results.append(cell)
        if cell_type and cell.get("type") == cell_type:
            results.append(cell)
    return results


def find_cell_by_label(data: dict, label: str) -> dict:
    cells = data["pages"][0]["cells"]
    for cell in cells:
        if cell.get("label") == label:
            return cell
    return None


def get_child_cells(data: dict, parent_id: str) -> list:
    cells = data["pages"][0]["cells"]
    return [c for c in cells if c.get("parent") == parent_id]


def remove_cell(data: dict, cell_id: str) -> None:
    cells = data["pages"][0]["cells"]
    # Remove the cell itself
    data["pages"][0]["cells"] = [c for c in cells if c["id"] != cell_id]
    # Remove any child cells
    data["pages"][0]["cells"] = [
        c for c in data["pages"][0]["cells"] if c.get("parent") != cell_id
    ]


def next_id(data: dict) -> str:
    """Generate a unique cell ID based on existing ones."""
    cells = data["pages"][0]["cells"]
    prefix = "6e32AYOivEadNJBoou7x-"
    existing_nums = []
    for c in cells:
        parts = c["id"].split("-")
        if len(parts) > 1 and parts[-1].isdigit():
            existing_nums.append(int(parts[-1]))
    next_num = max(existing_nums) + 1 if existing_nums else 1
    return f"{prefix}{next_num}"


def add_node(data: dict, label: str, parent: str = "1",
             node_type: str = "node") -> str:
    """Add a node cell to the diagram."""
    cell_id = next_id(data)
    cell = {
        "id": cell_id,
        "type": node_type,
        "parent": parent,
        "label": label
    }
    data["pages"][0]["cells"].append(cell)
    return cell_id


def make_enumeration(data: dict, class_cell: dict,
                     enum_values: list[str]) -> str:
    """Convert a class node to enumeration format."""
    # Remove all children (old attributes)
    children = get_child_cells(data, class_cell["id"])
    for child in children:
        remove_cell(data, child["id"])
    # Change label to enumeration format
    class_cell["label"] = f"«enumeration» {class_cell['label']}"
    # Add enum values as children
    for value in enum_values:
        add_node(data, value, parent=class_cell["id"])
    return class_cell["id"]


def correct_diagram(data: dict) -> dict:
    cells = data["pages"][0]["cells"]

    # 1. Convert Rol from class to enumeration
    rol_cell = find_cell_by_label(data, "Rol")
    if rol_cell:
        make_enumeration(data, rol_cell,
                         ["ADMIN", "PRODUCT_OWNER", "SCRUM_MASTER", "DEVELOPER"])
        print("✓ Rol convertido a enumeración")

    # 2. Remove validarLimiteWIP() from Usuario
    usuario_cell = find_cell_by_label(data, "Usuario")
    if usuario_cell:
        children = get_child_cells(data, usuario_cell["id"])
        for child in children:
            if "validarLimiteWIP" in child.get("label", ""):
                remove_cell(data, child["id"])
                print("✓ validarLimiteWIP() eliminado de Usuario")

    # 3. Fix TipoMensaje: remove MODULO and PRIVADO
    tipomensaje_cell = find_cell_by_label(data, "«enumeration» TipoMensaje")
    if not tipomensaje_cell:
        tipomensaje_cell = find_cell_by_label(data, "TipoMensaje")
    if tipomensaje_cell:
        # If it already has «enumeration» in label, it's already an enum
        children = get_child_cells(data, tipomensaje_cell["id"])
        for child in children:
            label = child.get("label", "")
            # Keep only PROYECTO and TAREA
            if label and label not in ("PROYECTO", "TAREA",
                                        "«enumeration» TipoMensaje"):
                # Check if this is a TipoMensaje child
                if child.get("type") == "node" and child.get("parent") == tipomensaje_cell["id"]:
                    remove_cell(data, child["id"])
                    print(f"✓ Eliminado {label} de TipoMensaje")

    # 4. Add Epica entity
    if not find_cell_by_label(data, "Epica"):
        epica_id = add_node(data, "Epica")
        add_node(data, "- id : UUID", parent=epica_id)
        add_node(data, "- titulo : String", parent=epica_id)
        add_node(data, "- descripcion : String", parent=epica_id)
        add_node(data, "- prioridad : Prioridad", parent=epica_id)
        add_node(data, "- estado : String", parent=epica_id)
        print("✓ Epica agregada")

        # Add edge: Epica (source) -> HistoriaUsuario (target)
        hu = find_cell_by_label(data, "HistoriaUsuario")
        if hu:
            edge_id = next_id(data)
            edge = {"id": edge_id, "type": "edge", "parent": "1",
                    "source": epica_id, "target": hu["id"], "label": "contiene"}
            data["pages"][0]["cells"].append(edge)
            add_node(data, "1", parent=edge_id)
            add_node(data, "0..*", parent=edge_id)
            print("✓ Relación Epica -> HistoriaUsuario agregada")

    # 5. Add TaskStateTransition entity
    if not find_cell_by_label(data, "TaskStateTransition"):
        tst_id = add_node(data, "TaskStateTransition")
        for attr in ["- id : UUID", "- taskId : UUID", "- fromEstado : EstadoTarea",
                      "- toEstado : EstadoTarea", "- timestamp : DateTime",
                      "- userId : UUID", "- reason : String"]:
            add_node(data, attr, parent=tst_id)
        print("✓ TaskStateTransition agregada")

    # 6. Add EstadoModulo enumeration
    if not find_cell_by_label(data, "«enumeration» EstadoModulo"):
        em_id = add_node(data, "«enumeration» EstadoModulo")
        for val in ["ACTIVO", "INACTIVO"]:
            add_node(data, val, parent=em_id)
        print("✓ EstadoModulo agregado")

    # 7. Fix Sprint -> Modulo relation to Sprint -> Proyecto
    # Find edge from Modulo to Sprint (source: Modulo, target: Sprint)
    modulo_cell = find_cell_by_label(data, "Modulo")
    sprint_cell = find_cell_by_label(data, "Sprint")
    proyecto_cell = find_cell_by_label(data, "Proyecto")
    if modulo_cell and sprint_cell and proyecto_cell:
        edges_to_update = []
        for cell in cells:
            if (cell.get("type") == "edge" and
                    cell.get("source") == modulo_cell["id"] and
                    cell.get("target") == sprint_cell["id"]):
                edges_to_update.append(cell)

        for edge in edges_to_update:
            # Change source from Modulo to Proyecto
            edge["source"] = proyecto_cell["id"]
            edge["label"] = "organiza"
            print("✓ Relación Sprint -> Proyecto corregida")

    # 8. Add HistoriaUsuario -> Modulo relation
    hu_cell = find_cell_by_label(data, "HistoriaUsuario")
    modulo_cell = find_cell_by_label(data, "Modulo")
    if hu_cell and modulo_cell:
        # Check if relation doesn't already exist
        exists = False
        for cell in cells:
            if (cell.get("type") == "edge" and
                    cell.get("source") == hu_cell["id"] and
                    cell.get("target") == modulo_cell["id"]):
                exists = True
                break
        if not exists:
            edge_id = next_id(data)
            edge = {"id": edge_id, "type": "edge", "parent": "1",
                    "source": hu_cell["id"], "target": modulo_cell["id"],
                    "label": "pertenece a"}
            data["pages"][0]["cells"].append(edge)
            add_node(data, "0..*", parent=edge_id)
            add_node(data, "1", parent=edge_id)
            print("✓ Relación HistoriaUsuario -> Modulo agregada")

    # 9. Remove PAUSADO from EstadoProyecto
    ep_cell = find_cell_by_label(data, "«enumeration» EstadoProyecto")
    if not ep_cell:
        ep_cell = find_cell_by_label(data, "EstadoProyecto")
    if ep_cell:
        children = get_child_cells(data, ep_cell["id"])
        for child in children:
            if child.get("label") == "PAUSADO":
                remove_cell(data, child["id"])
                print("✓ PAUSADO eliminado de EstadoProyecto")

    # 10. Remove limiteWIP from Proyecto
    if proyecto_cell:
        children = get_child_cells(data, proyecto_cell["id"])
        for child in children:
            if "limiteWIP" in child.get("label", ""):
                remove_cell(data, child["id"])
                print("✓ limiteWIP eliminado de Proyecto")

    return data


def main():
    if not os.path.exists(UML_PATH):
        print(f"Error: No se encuentra {UML_PATH}")
        return

    data = load_json(UML_PATH)
    data = correct_diagram(data)
    save_json(UML_PATH, data)
    print("\nCorrecciones aplicadas. Abre el archivo en Draw.io para verificar.")


if __name__ == "__main__":
    main()
