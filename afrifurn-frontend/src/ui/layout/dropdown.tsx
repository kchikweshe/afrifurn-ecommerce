import { Component, type JSX } from "react";

// DropdownComponent.tsx
export abstract class DropdownComponent extends Component {
    abstract renderDropdownContent(): JSX.Element;
  
    render() {
      return (
        <div className="dropdown">
          {this.renderDropdownContent()}
        </div>
      );
    }
  }

  
