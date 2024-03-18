#!/usr/bin/python3
"""Defines the HBNBCommand class serves as the console for the project."""
import cmd
import os
import json
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.amenity import Amenity
from models.city import City
from models.review import Review
from models.state import State
from models.place import Place


class HBNBCommand(cmd.Cmd):
    """A command-line interpreter for managing objects in the project."""

    prompt = "(hbnb) "
    class_names_list = [
        "BaseModel",
        "User",
        "State",
        "City",
        "Amenity",
        "Place",
        "Review",
    ]
    func_list = [
        "quit",
        "show",
        "all",
        "create",
        "destroy",
        "update",
        "EOF",
        "count"
    ]
    class_attr = ["id", "created_at", "updated_at"]

    def do_quit(self, line):
        """Quit command to exit the program"""
        exit()

    def precmd(self, line: str) -> str:
        """Prepares the command line for execution"""
        if "." in line and "(" in line:
            pre_line_list = line.split(".")
            class_name = pre_line_list[0]
            second_part = pre_line_list[1]
            func_name = second_part.split('(')[0]
            if "(" in second_part:
                parentheses = second_part.split("(")[1]
                if ")" in parentheses:
                    class_id = parentheses.split(")")[0]
                    if class_id.startswith('"') and class_id.endswith('"'):
                        class_id = class_id.strip('"')
                    if func_name in self.func_list:
                        new_line = f"{func_name} {class_name} {class_id}"
                        if func_name == "update":
                            attr_name, attr_val = parentheses.rsplit(", ", 1)
                            attr_val = attr_val.strip(")")
                            new_line += f" {attr_name} {attr_val}"
                        return new_line
            else:
                if func_name in self.func_list:
                    new_line = func_name + " " + class_name
                    return new_line
        return line

    def do_create(self, args):
        """Creates a new instance of a specified class"""
        if not args:
            print("** class name missing **")
            return
        args_list = args.split()
        class_name = args_list[0]
        if class_name not in self.class_names_list:
            print("** class doesn't exist **")
        else:
            new_instance = eval(class_name)()
            storage.save()
            print(new_instance.id)

    def do_count(self, args):
        """Counts the number of instances of a specified class"""
        storage.reload()
        args_list = args.split()
        class_name = args_list[0]
        all_objs = storage.all()
        if class_name in self.class_names_list:
            filtered_objs = [obj for obj in all_objs.values()
                             if obj.__class__.__name__ == class_name]
            if filtered_objs != 0:
                print(len(filtered_objs))
            return
        return

    def do_show(self, args):
        """Displays details of a specified instance"""
        if not args:
            print("** class name missing **")
            return

        args_list = args.split()
        class_name = args_list[0]
        if class_name not in self.class_names_list:
            print("** class doesn't exist **")
            return

        if len(args_list) < 2:
            print("** instance id missing **")
            return
        instance_id = args_list[1]
        storage.reload()
        all_objs = storage.all()
        key = f"{class_name}.{instance_id}"
        if key not in all_objs:
            print("** no instance found **")
            return
        else:
            print(all_objs[key])

    def do_destroy(self, args):
        """Deletes a specified instance"""
        if not args:
            print("** class name missing **")
            return
        args_list = args.split()
        class_name = args_list[0]

        if class_name not in self.class_names_list:
            print("** class doesn't exist **")
            return
        if len(args_list) < 2:
            print("** instance id missing **")
            return
        instance_id = args_list[1]
        storage.reload()
        all_objs = storage.all()
        key = f"{class_name}.{instance_id}"
        if key not in all_objs:
            print("** no instance found **")
            return
        else:
            del all_objs[key]
            storage.save()

    def do_all(self, args):
        """Displays details of all instances or of a specified class"""
        storage.reload()

        if not args:
            all_objs = storage.all()
            for obj in all_objs.values():
                print(obj)
            return
        else:
            args_list = args.split()
            class_name = args_list[0]

            if class_name not in self.class_names_list:
                print("** class doesn't exist **")
                return

            all_objs = storage.all()
            filtered_objs = [obj for obj in all_objs.values()
                             if obj.__class__.__name__ == class_name]
            for obj in filtered_objs:
                print(obj)

    def do_update(self, args):
        """Updates attributes of specified instance"""
        if not args:
            print("** class name missing **")
            return
        args_list = args.split()
        class_name = args_list[0]
        if class_name not in self.class_names_list:
            print("** class doesn't exist **")
            return
        if len(args_list) < 2:
            print("** instance id missing **")
            return
        instance_id = args_list[1]
        storage.reload()
        all_objs = storage.all()
        key = f"{class_name}.{instance_id}"
        if key not in all_objs:
            print("** no instance found **")
            return
        if len(args_list) < 3:
            print("** attribute name missing **")
            return
        if len(args_list) < 4:
            print("** value missing **")
            return
        attr_name = args_list[2]
        if attr_name in self.class_attr:
            return

        attr_value = json.loads(args_list[3])

        if isinstance(attr_value, str) and attr_value.isdigit():
            attr_value = int(attr_value)

        setattr(all_objs[key], attr_name, attr_value)
        storage.save()

    def do_EOF(self, line):
        """Exits the application"""
        print()
        exit()

    def do_help(self, arg: str):
        """Displays help information"""
        return super().do_help(arg)

    def emptyline(self) -> bool:
        """Handles empty lines"""
        pass

    def do_clear(self, args):
        """Clears the console screen"""
        os.system("clear")


if __name__ == "__main__":
    HBNBCommand().cmdloop()
